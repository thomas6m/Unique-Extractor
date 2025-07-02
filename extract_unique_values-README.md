# Runbook for Unique Values Extractor Script

## Overview

This script extracts unique values from a specified field in tabular data (CSV, JSON, YAML, Parquet). It supports filtering rows, output formatting (CSV, JSON, YAML, Parquet), and flexible input/output configuration via CLI or YAML config file.

## Prerequisites

- **Python 3.8+**
- **Required Python packages:**
  - `polars`
  - `pyyaml`
  - `psutil`
- **Input files supported:** `.csv`, `.json`, `.yaml/.yml`, `.parquet`
- **Permissions** to read input files and write output files

## Setup

### 1. Install dependencies

```bash
pip install polars pyyaml psutil
```

### 2. Prepare input data

- Place your input file in an accessible directory
- **Supported formats:** CSV, JSON, YAML, Parquet
- **(Optional)** Create a YAML config file for complex configurations

## Usage

### Command Line Interface (CLI)

```bash
python script.py --input INPUT_FILE --output OUTPUT_FILE --unique-field FIELD_NAME [OPTIONS]
```

#### Required arguments

- `--input`: Path to input file
- `--output`: Path to output file
- `--unique-field`: Field name to extract unique values from

#### Common optional arguments

- `--filters`: Filters to apply (e.g., `status=active`, `age>=30`), multiple allowed
- `--delimiter`: CSV delimiter (default: `,`)
- `--separator`: Separator for multi-value fields (default: `;`)
- `--column-name`: Override column name in output (default: same as unique field)
- `--row-format`: `single` (all values concatenated) or `multi` (each unique value in separate row), default: `single`
- `--output-format`: Output format, one of `csv`, `json`, `yaml`, `parquet` (default: `csv`)
- `--drop-na`: Drop rows where unique field is null
- `--dry-run`: Run without saving output, print preview instead
- `--log-level`: Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`), default `INFO`
- `--config`: YAML config file path to load configuration
- `--print-config-template`: Print example YAML config and exit

### Example CLI commands

#### Extract unique active emails from CSV, output as JSON:

```bash
python script.py --input users.csv --output emails.json --unique-field email --filters "status=active" --output-format json
```

#### Extract unique values from YAML with multi-row output and dry-run:

```bash
python script.py --input data.yaml --output result.csv --unique-field id --row-format multi --dry-run
```

#### Load configuration from YAML file and override output file:

```bash
python script.py --config config.yaml --output new_output.csv
```

#### Print config template:

```bash
python script.py --print-config-template
```

## YAML Config File Structure

### Example:

```yaml
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
```

## Filters Syntax

Filters are applied in the form:

```
field<operator>value1,value2,...
```

### Supported operators:

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals | `status=active` |
| `!=` | Not equals | `status!=inactive` |
| `>` | Greater than | `age>30` |
| `<` | Less than | `age<65` |
| `>=` | Greater or equal | `age>=18` |
| `<=` | Less or equal | `age<=60` |
| `~` | Regex contains | `name~john,doe` |

## Logging

- Logs are stored in `logs/extractor.log`
- Logs also output to console
- Default log level is `INFO`, adjustable with `--log-level`

## Error Handling

### Exit codes:

| Code | Reason |
|------|--------|
| 0 | Success |
| 1 | Configuration error |
| 2 | Input file not found/error |
| 3 | Processing error (filter, missing fields) |
| 4 | Output saving error |
| 99 | Unexpected error |

Errors are logged and printed to console.

## Performance and Resource Use

- Uses `polars` for fast processing
- Memory usage logged before and after processing
- Supports filtering to reduce data size before extraction

## Troubleshooting

- **File not found:** Check file paths and permissions
- **Unsupported format:** Only CSV, JSON, YAML, Parquet are supported
- **Filter parsing errors:** Verify filter syntax
- **Output issues:** Check output format support and directory permissions
- **High memory use:** Use filters or smaller input files

## Maintenance Tips

- Update dependencies regularly (`polars`, `pyyaml`, `psutil`)
- Add new file formats or output formats if needed
- Extend filter operators for more complex queries
- Monitor logs for recurring issues
