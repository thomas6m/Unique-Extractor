import polars as pl
import argparse
import os
import sys
import logging
import time
import psutil
import yaml  # for YAML reading fallback

# ------------------------- Logging Setup ------------------------- #
logging.basicConfig(
    filename='extractor.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ------------------------- File Reading Function ------------------------- #
def read_input_file(input_file: str, delimiter: str):
    """Auto-detect file format based on file extension."""
    file_extension = input_file.split('.')[-1].lower()

    if file_extension == 'csv':
        return pl.read_csv(input_file, separator=delimiter)
    elif file_extension == 'json':
        return pl.read_json(input_file)
    elif file_extension == 'parquet':
        return pl.read_parquet(input_file)
    elif file_extension in ('yaml', 'yml'):
        # polars does not support YAML natively; read with PyYAML then convert
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)
        return pl.from_dicts(data if isinstance(data, list) else [data])
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

# ------------------------- Filter Parsing ------------------------- #
def parse_cli_filters(filters_raw) -> dict:
    filters = {}
    for arg in filters_raw:
        if "=" not in arg:
            continue
        key, value = arg.split("=", 1)
        filters[key.strip()] = [v.strip() for v in value.split(",") if v.strip()]
    return filters

def prompt_filters(columns: list[str], df: pl.DataFrame) -> dict:
    print("\n📌 Available fields:", ', '.join(columns))
    filters = {}
    while True:
        field = input("Field name (leave empty to stop): ").strip()
        if not field:
            break
        if field not in columns:
            print(f"❌ '{field}' is not a valid column.")
            continue

        # Show distinct values for this field
        distinct_vals = df.select(pl.col(field).unique()).to_series().drop_nulls().to_list()
        distinct_vals_str = ', '.join(str(v) for v in distinct_vals)
        print(f"🔹 Available values for '{field}': {distinct_vals_str}")

        values = input(f"Enter comma-separated values for {field}: ").strip()
        filters[field] = [v.strip() for v in values.split(",") if v.strip()]
    return filters

# ------------------------- Prompt Options ------------------------- #
def prompt_unique_field(columns: list[str]) -> str:
    print("\n🎯 Available fields:", ', '.join(columns))
    while True:
        field = input("Select the field to extract unique values from: ").strip()
        if field in columns or field == "contact_ids":
            return field
        print(f"❌ Invalid field '{field}'. Try again.")

def prompt_separator(default_sep: str = ";") -> str:
    sep = input(f"Enter separator for unique values (default '{default_sep}'): ").strip()
    return sep if sep else default_sep

def prompt_column_name(default_col: str) -> str:
    name = input(f"Enter custom column name (default '{default_col}'): ").strip()
    return name if name else default_col

def prompt_row_format() -> str:
    while True:
        choice = input("Row format? (single/multi) [default=single]: ").strip().lower()
        if choice in {"", "single"}:
            return "single"
        elif choice == "multi":
            return "multi"
        else:
            print("Invalid option. Choose 'single' or 'multi'.")

def prompt_output_format() -> str:
    """Prompt user for output file format."""
    while True:
        fmt = input("Select output format (csv, json, yaml, parquet) [default=csv]: ").strip().lower()
        if fmt in {"csv", "json", "yaml", "parquet"}:
            return fmt
        elif fmt == "":
            return "csv"
        else:
            print("❌ Invalid format. Choose from csv, json, yaml, parquet.")

# ------------------------- Core Processing ------------------------- #
def filter_and_extract(input_file: str, filters: dict, unique_field: str, delimiter: str) -> pl.Series:
    filter_columns = list(filters.keys())
    needed_columns = set(filter_columns + [unique_field])

    # Auto-detect the file format and read accordingly
    df = read_input_file(input_file, delimiter)

    # Lazy frame (processing)
    lf = df.lazy()

    for col in needed_columns:
        lf = lf.with_columns(pl.col(col).cast(pl.Utf8).str.strip_chars().alias(col))
        lf = lf.filter(pl.col(col).is_not_null() & (pl.col(col) != ""))

    for field, vals in filters.items():
        lf = lf.filter(pl.col(field).is_in(vals))

    if unique_field == "contact_ids":
        lf = (
            lf
            .with_columns(pl.col("contact_ids").str.split(",").alias("contact_list"))
            .explode("contact_list")
            .with_columns(pl.col("contact_list").str.strip_chars().alias("contact"))
            .filter(pl.col("contact").is_not_null() & (pl.col("contact") != ""))
        )
        result = lf.select(pl.col("contact").unique()).collect()
        return result["contact"]
    else:
        result = lf.select(pl.col(unique_field).unique()).collect()
        return result[unique_field]

# ------------------------- Output Save ------------------------- #
def save_output(series: pl.Series, filters: dict, unique_field: str, output_file: str,
                separator: str, row_format: str, column_name: str, output_format: str = "csv"):
    try:
        if os.path.exists(output_file):
            confirm = input(f"⚠️ File '{output_file}' exists. Overwrite? (y/n): ").strip().lower()
            if confirm not in ("y", "yes"):
                print("❌ Aborted by user.")
                return

        if row_format == "single":
            out_df = pl.DataFrame({
                "filters": [", ".join(f"{k}={','.join(v)}" for k, v in filters.items())],
                column_name: [separator.join(series.to_list())]
            })
        else:
            out_df = pl.DataFrame({column_name: series})

        if output_format == "csv":
            out_df.write_csv(output_file)
        elif output_format == "json":
            out_df.write_json(output_file)
        elif output_format == "yaml":
            out_df.write_yaml(output_file)
        elif output_format == "parquet":
            out_df.write_parquet(output_file)
        else:
            print(f"❌ Unsupported output format: {output_format}")
            return

        logging.info(f"Saved output to: {output_file}")
        print(f"\n✅ Output saved to: {output_file}")
    except Exception as e:
        logging.error(f"Failed to save output: {e}", exc_info=True)
        print(f"❌ Failed to save output: {e}")

# ------------------------- Main Entry Point ------------------------- #
def main():
    parser = argparse.ArgumentParser(description="Extract unique values from various file formats.")
    parser.add_argument("--input", help="Input file path (CSV, JSON, YAML, or Parquet)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--unique-field", help="Field name to extract unique values from")
    parser.add_argument("--separator", help="Separator for single-row output")
    parser.add_argument("--column-name", help="Custom column name for output")
    parser.add_argument("--row-format", choices=["single", "multi"], help="Output format: single or multi")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter (default=',')")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("filters", nargs="*", help="Filters in format field=value1,value2,...")

    args = parser.parse_args()

    # Prompt for input file if missing
    if not args.input:
        args.input = input("📂 Enter path to input file (CSV, JSON, YAML, or Parquet): ").strip()

    start_time = time.time()
    logging.info(f"Script started with input: {args.input}")

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists(args.input):
        logging.error(f"Input file '{args.input}' does not exist.")
        print(f"❌ Input file '{args.input}' does not exist.")
        sys.exit(1)

    try:
        df_preview = read_input_file(args.input, args.delimiter)
        columns = df_preview.columns
    except Exception as e:
        logging.error(f"Failed to read input file: {e}", exc_info=True)
        print(f"❌ Error reading input file: {e}")
        sys.exit(1)

    filters = parse_cli_filters(args.filters) if args.filters else prompt_filters(columns, df_preview)

    # Validate filter columns
    for col in filters.keys():
        if col not in columns:
            print(f"❌ Column '{col}' not found in input file.")
            sys.exit(1)

    # Unique field
    unique_field = args.unique_field if args.unique_field else prompt_unique_field(columns)
    if unique_field not in columns and unique_field != "contact_ids":
        print(f"❌ Unique field '{unique_field}' is not in the input file.")
        sys.exit(1)

    # Separator
    separator = args.separator if args.separator else prompt_separator()

    # Column name
    default_col_name = f"unique_{unique_field}"
    column_name = args.column_name if args.column_name else prompt_column_name(default_col_name)

    # Row format
    row_format = args.row_format if args.row_format else prompt_row_format()

    try:
        result_series = filter_and_extract(args.input, filters, unique_field, args.delimiter)
    except Exception as e:
        logging.error(f"Filtering failed: {e}", exc_info=True)
        print(f"❌ Filtering failed: {e}")
        sys.exit(1)

    if result_series.is_empty():
        print("ℹ️ No matching values found.")
        return

    print("\n🔎 Unique values found:")
    for val in result_series.to_list():
        print(f" - {val}")

    if args.output:
        # Infer output format from file extension if possible
        ext = args.output.split('.')[-1].lower()
        output_fmt = ext if ext in {"csv", "json", "yaml", "parquet"} else "csv"
        save_output(result_series, filters, unique_field, args.output, separator, row_format, column_name, output_fmt)
    else:
        save = input("\n💾 Save results? (y/n): ").lower().strip()
        if save in ("y", "yes"):
            out_path = input("Output file name (without extension): ").strip()
            output_format = prompt_output_format()

            # Append extension if not present
            if not out_path.lower().endswith(f".{output_format}"):
                out_path += f".{output_format}"

            save_output(result_series, filters, unique_field, out_path, separator, row_format, column_name, output_format)

    elapsed = time.time() - start_time
    mem_used = psutil.Process().memory_info().rss / (1024 * 1024)
    print(f"\n⏱️ Time taken: {elapsed:.2f}s | 🧠 Memory used: {mem_used:.2f} MB")
    logging.info(f"Time: {elapsed:.2f}s, Memory: {mem_used:.2f} MB")

if __name__ == "__main__":
    main()
