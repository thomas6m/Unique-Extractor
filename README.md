# Unique Value Extractor

A powerful command-line tool to extract unique values from tabular data files (CSV, JSON, YAML, Parquet) with flexible filtering and output options.

## Features

- Supports multiple input formats: CSV, JSON, YAML, Parquet
- Extract unique values from any specified column
- Advanced filtering with operators: `=`, `!=`, `>`, `<`, `>=`, `<=`, regex match `~`
- Supports multi-value fields with custom separators
- Output results in CSV, JSON, YAML, or Parquet format
- Drop rows with null values in the target column
- Dry-run mode to preview output without saving
- Configurable via command-line arguments or YAML config file
- Detailed logging with file and console output

## Installation

Requires Python 3.7+ and the following packages:
- polars
- pyyaml
- psutil

Install dependencies with:
```bash
pip install polars pyyaml psutil
```

## Usage

```bash
python extractor.py --input input.csv --output output.csv --unique-field email [options]
```

### Required Arguments

- `--input` — Input file path (CSV, JSON, YAML, Parquet)
- `--output` — Output file path
- `--unique-field` — Column name to extract unique values from

### Optional Arguments

- `--filters` — Filters to apply, e.g. `status=active`, `age>=30`, `name~^John`
- `--delimiter` — CSV delimiter in input file (default: `,`)
- `--separator` — Separator used inside multi-value fields (default: `;`)
- `--column-name` — Override output column name (defaults to unique field)
- `--row-format` — Output format style: `single` (one row, values joined) or `multi` (one row per value)
- `--output-format` — Output file format: `csv`, `json`, `yaml`, `parquet` (default: `csv`)
- `--drop-na` — Drop rows where unique field is null
- `--dry-run` — Process without saving output, prints preview
- `--log-level` — Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`)
- `--config` — Load configuration from YAML file
- `--print-config-template` — Print a sample YAML config and exit

## Filters Syntax

Filters are specified as strings with the format:
```
field operator value[,value2,...]
```

### Supported operators:

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals (exact match) | `status=active` |
| `!=` | Not equals | `status!=inactive` |
| `>` | Greater than (numeric) | `age>30` |
| `<` | Less than (numeric) | `age<50` |
| `>=` | Greater or equal | `score>=80` |
| `<=` | Less or equal | `score<=100` |
| `~` | Regex contains | `name~^John` (starts with John) |

Multiple values can be comma-separated:
```
status=active,pending
```

## Example CLI Usage

### Extract unique emails from users.csv where status is active and age is over 30:
```bash
python extractor.py \
  --input users.csv \
  --output active_emails.csv \
  --unique-field email \
  --filters "status=active" "age>30" \
  --drop-na
```

### Extract unique tags from a multi-value tags column, outputting one value per row in JSON:
```bash
python extractor.py \
  --input data.json \
  --output tags.json \
  --unique-field tags \
  --row-format multi \
  --output-format json \
  --separator ","
```

## YAML Configuration Example

You can specify all options in a YAML file:
```yaml
input_file: "input.csv"
output_file: "output.csv"
unique_field: "email"
filters:
  - ["status", "=", ["active"]]
  - ["age", ">", ["30"]]
separator: ";"
row_format: "single"
output_format: "csv"
delimiter: ","
drop_na: false
dry_run: false
```

Run with:
```bash
python extractor.py --config config.yaml
```

## Logging

Logs are saved in the `logs` directory as `extractor.log`. Logs also print to console.

## Development & Contribution

Contributions welcome! Feel free to open issues or submit pull requests.

## License

MIT License
