#!/usr/bin/env python3

import polars as pl
import argparse
import os
import sys
import logging
import time
import psutil
import yaml
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union
from dataclasses import dataclass

# ---------------- Configuration ---------------- #
@dataclass
class ExtractorConfig:
    input_file: str
    output_file: str
    unique_field: str
    separator: str = ";"
    column_name: Optional[str] = None
    row_format: str = "single"
    output_format: str = "csv"
    delimiter: str = ","
    delimiter_regex: Optional[str] = None
    filters: List[Tuple[str, str, List[str]]] = None
    drop_na: bool = False
    dry_run: bool = False

    def __post_init__(self):
        self.filters = self.filters or []
        if self.column_name is None:
            self.column_name = self.unique_field

# ---------------- Logging ---------------- #
def setup_logging(level: str = "INFO"):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    handlers = [
        logging.FileHandler(log_dir / "extractor.log"),
        logging.StreamHandler(sys.stdout)
    ]
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers
    )

# ---------------- File I/O ---------------- #
def validate_file_path(path: str) -> Path:
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not p.is_file():
        raise ValueError(f"Path is not a file: {path}")
    return p

def read_input_file(path: Path, delimiter: str) -> pl.DataFrame:
    ext = path.suffix.lower()
    size_mb = path.stat().st_size / (1024 * 1024)
    logging.info(f"Reading {ext} file: {path.name} ({size_mb:.2f} MB)")
    try:
        if ext == ".csv":
            return pl.read_csv(path, separator=delimiter, ignore_errors=True,
                               truncate_ragged_lines=True, infer_schema_length=10000)
        if ext == ".json":
            try:
                return pl.read_ndjson(path)
            except:
                return pl.read_json(path)
        if ext in {".yml", ".yaml"}:
            raw = yaml.safe_load(path.open("r", encoding="utf-8"))
            rows = raw if isinstance(raw, list) else [raw]
            return pl.DataFrame([flatten_dict(r) for r in rows if r is not None])
        if ext == ".parquet":
            return pl.read_parquet(path)
    except Exception as e:
        logging.error(f"Failed to read {path}: {e}")
        raise
    raise ValueError(f"Unsupported file format: {ext}")

def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    if not isinstance(d, dict):
        return {parent_key or "value": d}
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i, item in enumerate(v):
                items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# ---------------- Filter Logic ---------------- #
class FilterParser:
    OPS = [">=", "<=", "!=", "=", ">", "<", "~"]

    @classmethod
    def parse(cls, expressions: List[str]) -> List[Tuple[str, str, List[str]]]:
        valid = []
        for expr in expressions:
            m = re.match(r"(.+?)(>=|<=|!=|=|>|<|~)(.+)", expr.strip())
            if not m:
                logging.warning(f"Skipping invalid filter: {expr}")
                continue
            field, op, vals = m.groups()
            vals_list = [v.strip() for v in vals.split(",") if v.strip()]
            if not vals_list:
                logging.warning(f"No values in filter: {expr}")
                continue
            valid.append((field.strip(), op, vals_list))
            logging.info(f"Parsed filter: {field.strip()} {op} {vals_list}")
        return valid

class FilterApplier:
    @staticmethod
    def apply(lf: pl.LazyFrame, field: str, op: str, vals: List[str]) -> pl.LazyFrame:
        if field not in lf.schema:
            raise ValueError(f"Field '{field}' not found in input schema")
        col = pl.col(field)

        if op in {">", "<", ">=", "<="}:
            try:
                val = float(vals[0])
                return lf.filter(getattr(col.cast(pl.Float64, strict=False), op)(val))
            except ValueError:
                raise ValueError(f"Cannot convert '{vals[0]}' to float for filter '{op}'")
        col = col.cast(pl.Utf8).str.strip_chars()
        if op == "=":
            return lf.filter(col.is_in(vals))
        if op == "!=":
            return lf.filter(~col.is_in(vals))
        if op == "~":
            pattern = "|".join(re.escape(v) for v in vals)
            return lf.filter(col.str.contains(pattern, literal=False))
        raise ValueError(f"Unsupported operator: {op}")

# ---------------- Processing ---------------- #
def process_multi(df: pl.DataFrame, field: str, sep: str) -> pl.Series:
    return (
        df.lazy()
        .select(pl.col(field).str.split(sep).explode().str.strip_chars())
        .filter(pl.col(field).is_not_null() & (pl.col(field) != ""))
        .unique().sort(field)
        .collect().get_column(field)
    )

def extract_unique_values(cfg: ExtractorConfig) -> pl.Series:
    df = read_input_file(validate_file_path(cfg.input_file), cfg.delimiter)
    logging.info(f"Loaded {df.height} rows × {df.width} columns")
    if cfg.unique_field not in df.columns:
        raise ValueError(f"Unique field missing: {cfg.unique_field}")
    lf = df.lazy()
    for f, op, vals in cfg.filters:
        lf = FilterApplier.apply(lf, f, op, vals)
    if cfg.drop_na:
        lf = lf.filter(pl.col(cfg.unique_field).is_not_null())
    filtered = lf.collect()
    logging.info(f"After filter: {filtered.height} rows")
    if cfg.row_format == "multi":
        return process_multi(filtered, cfg.unique_field, cfg.separator)
    return (
        filtered.lazy()
        .select(pl.col(cfg.unique_field).cast(pl.Utf8).str.strip_chars().unique().drop_nulls())
        .sort(cfg.unique_field)
        .collect().get_column(cfg.unique_field)
    )

# ---------------- Output ---------------- #
def save_output(series: pl.Series, cfg: ExtractorConfig):
    try:
        out = Path(cfg.output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        meta = {
            "field": cfg.unique_field,
            "filters": cfg.filters or [],
            "count": len(series),
            "time": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        if cfg.row_format == "single":
            df = pl.DataFrame({"meta": [str(meta)], cfg.column_name: [cfg.separator.join(series.to_list())]})
        else:
            items = [{cfg.column_name: v} for v in series.to_list()]
            df = pl.DataFrame([{"meta": str(meta), cfg.column_name: "METADATA"}] + items)
        if cfg.dry_run:
            print("Dry run mode - output not written")
            print(df.head(5))
            return
        if cfg.output_format == "csv":
            df.write_csv(out)
        elif cfg.output_format == "json":
            df.write_json(out, pretty=True)
        elif cfg.output_format == "yaml":
            yaml.safe_dump(df.to_dicts(), out.open("w"), default_flow_style=False)
        elif cfg.output_format == "parquet":
            df.write_parquet(out)
        else:
            raise ValueError(f"Unsupported format: {cfg.output_format}")
        logging.info(f"Output written: {out}")
        print(f"✅ Saved to {out}")
    except Exception as e:
        logging.error(f"Failed to save output: {e}")
        raise

# ---------------- Main CLI ---------------- #
def get_memory_mb() -> float:
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def load_config_from_yaml(yaml_path: str) -> dict:
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    p = argparse.ArgumentParser(description="Extract unique values from tabular data")
    p.add_argument("--input", help="Input file path (CSV, JSON, YAML, Parquet)")
    p.add_argument("--output", help="Output file path")
    p.add_argument("--unique-field", help="Field to extract unique values from")
    p.add_argument("--filters", nargs="*", default=[], help="Filters in the form field=val or field>=val")
    p.add_argument("--delimiter", default=",", help="CSV delimiter (default: ,)")
    p.add_argument("--separator", default=";", help="Separator for multiple values (e.g., contact_ids)")
    p.add_argument("--column-name", help="Override column name in output")
    p.add_argument("--row-format", choices=["single", "multi"], default="single")
    p.add_argument("--output-format", choices=["csv", "json", "yaml", "parquet"], default="csv")
    p.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
    p.add_argument("--drop-na", action="store_true", help="Drop rows where unique field is null")
    p.add_argument("--dry-run", action="store_true", help="Run without saving output")
    p.add_argument("--config", help="Load configuration from YAML file")

    # New option to print config template
    p.add_argument(
        "--print-config-template",
        action="store_true",
        help="Print a sample YAML config template and exit"
    )

    args = p.parse_args()

    if args.print_config_template:
        sample_yaml = """
input_file: "input.csv"
output_file: "output.csv"
unique_field: "email"
filters:
  - ["status", "=", ["active"]]
separator: ";"
row_format: "single"
output_format: "csv"
delimiter: ","
drop_na: false
dry_run: false
"""
        print(sample_yaml)
        sys.exit(0)

    setup_logging(args.log_level)

    if args.config:
        cfg_dict = load_config_from_yaml(args.config)
        # Override YAML config fields with CLI args if provided
        if args.input is not None:
            cfg_dict["input_file"] = args.input
        if args.output is not None:
            cfg_dict["output_file"] = args.output
        if args.unique_field is not None:
            cfg_dict["unique_field"] = args.unique_field
        if args.separator is not None:
            cfg_dict["separator"] = args.separator
        if args.column_name is not None:
            cfg_dict["column_name"] = args.column_name
        if args.row_format is not None:
            cfg_dict["row_format"] = args.row_format
        if args.output_format is not None:
            cfg_dict["output_format"] = args.output_format
        if args.delimiter is not None:
            cfg_dict["delimiter"] = args.delimiter
        if args.filters:
            cfg_dict["filters"] = FilterParser.parse(args.filters)
        if args.drop_na:
            cfg_dict["drop_na"] = True
        if args.dry_run:
            cfg_dict["dry_run"] = True
        
        try:
            cfg = ExtractorConfig(**cfg_dict)
        except Exception as e:
            logging.error(f"Configuration error: {e}")
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    else:
        try:
            cfg = ExtractorConfig(
                args.input,
                args.output,
                args.unique_field,
                args.separator,
                args.column_name,
                args.row_format,
                args.output_format,
                args.delimiter,
                FilterParser.parse(args.filters),
                args.drop_na,
                args.dry_run
            )
        except Exception as e:
            logging.error(f"Configuration error: {e}")
            print(f"❌ Configuration error: {e}")
            sys.exit(1)

    logging.info(f"Config: {cfg}")
    start_mem = get_memory_mb()
    start = time.time()

    try:
        series = extract_unique_values(cfg)
    except FileNotFoundError as e:
        logging.error(f"Input file error: {e}")
        print(f"❌ Input file error: {e}")
        sys.exit(2)
    except ValueError as e:
        logging.error(f"Processing error: {e}")
        print(f"❌ Processing error: {e}")
        sys.exit(3)
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"❌ Unexpected error: {e}")
        sys.exit(99)

    try:
        save_output(series, cfg)
    except Exception as e:
        print(f"❌ Output error: {e}")
        sys.exit(4)

    elapsed = time.time() - start
    end_mem = get_memory_mb()
    print(f"⏱ {elapsed:.2f}s | 🧠 memory Δ {end_mem - start_mem:+.1f} MB | ✅ {len(series)} unique values")
    sys.exit(0)

if __name__ == "__main__":
    main()
