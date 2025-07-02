# extractor.py Runbook

## Overview

The `extractor.py` script is a data processing tool designed to:

- Load structured data from various formats (CSV, JSON, YAML, Parquet)
- Extract unique values from a specified column (`unique_field`)
- Apply filters, handle multi-value fields, clean up whitespace, and optionally drop nulls
- Output the result in your chosen format (CSV, JSON, YAML, or Parquet)

## Quick Start

### Basic Usage

```bash
python extractor.py \
  --input <input_file_path> \
  --output <output_file_path> \
  --unique-field <column_name>
```

### Full Command Syntax

```bash
python extractor.py \
  --input <input_file_path> \
  --output <output_file_path> \
  --unique-field <column_name> \
  [--filters <filter1> <filter2> ...] \
  [--delimiter <char>] \
  [--separator <char>] \
  [--column-name <output_column>] \
  [--row-format single|multi] \
  [--output-format csv|json|yaml|parquet] \
  [--log-level DEBUG|INFO|WARNING|ERROR] \
  [--drop-na] \
  [--dry-run]
```

### Example

```bash
python extractor.py \
  --input data.csv \
  --output result.csv \
  --unique-field email \
  --filters "country=US" "status!=inactive" \
  --drop-na \
  --output-format csv
```

## Arguments Reference

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `--input` | Path to input file (CSV, JSON, YAML, Parquet) | ✅ | — |
| `--output` | Path to save the output | ✅ | — |
| `--unique-field` | Column to extract unique values from | ✅ | — |
| `--filters` | List of filters (e.g., `age>30`, `status=active`) | ❌ | `[]` |
| `--delimiter` | Input file delimiter (for CSV) | ❌ | `,` |
| `--separator` | Multi-value field separator | ❌ | `;` |
| `--column-name` | Column name for output | ❌ | Same as `unique-field` |
| `--row-format` | Output row format: `single` or `multi` | ❌ | `single` |
| `--output-format` | Output file format | ❌ | `csv` |
| `--log-level` | Logging level | ❌ | `INFO` |
| `--drop-na` | Exclude null values in output | ❌ | `False` |
| `--dry-run` | Run without writing output file | ❌ | `False` |

## Supported File Formats

### Input Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| CSV | `.csv` | Must match `--delimiter` |
| JSON | `.json` | Supports JSON arrays and NDJSON |
| YAML | `.yaml`, `.yml` | Will be flattened |
| Parquet | `.parquet` | Natively supported |

### Output Formats

- **CSV**: Standard CSV file with extracted values
- **JSON**: List of dictionaries, optionally with metadata
- **YAML**: YAML output, useful for configurations
- **Parquet**: Efficient columnar storage format

## Filtering

### Filter Syntax

```bash
--filters "age>30" "status=active" "country!=US" "name~john"
```

### Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `status=active` |
| `!=` | Not equals | `status!=inactive` |
| `>` | Greater than | `age>30` |
| `<` | Less than | `age<65` |
| `>=` | Greater than or equal | `score>=80` |
| `<=` | Less than or equal | `score<=100` |
| `~` | Regex match | `name~john` |

### Multiple Values

For `=` and `!=` operators, you can specify multiple values using comma separation:

```bash
--filters "country=US,CA,UK"
```

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| `FileNotFoundError` | Invalid input path | Check `--input` path exists |
| `ValueError: Path is not a file` | Path is a directory | Provide file path, not directory |
| `Unsupported file format` | Unknown file extension | Use supported file types |
| `Field '<name>' not found in input schema` | Invalid `--unique-field` | Check column name spelling/case |
| `Unsupported operator` | Invalid filter operator | Use supported operators: `= != > < >= <= ~` |
| `dry run mode - output not written` | `--dry-run` flag is set | Remove `--dry-run` flag to save output |

## Logging

- Logs are saved to `logs/extractor.log`  
- Console logs are also printed to stdout
- Logging level is controlled by `--log-level`

Available log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Performance Monitoring

After each run, the script reports:

- Time taken
- Memory usage delta  
- Number of unique values extracted

**Example output:**
```
⏱ 2.34s | 🧠 memory Δ +18.7 MB | ✅ 223 unique values
```

## Best Practices

- **Validate first**: Use `--dry-run` to test filters before running full extraction
- **Clean data**: Use `--drop-na` to exclude blanks/nulls from output
- **Format optimization**: Use `--row-format multi` for one value per line (useful for IDs)
- **Audit trail**: Keep logs for debugging and auditing purposes
- **Performance**: For large datasets, consider using Parquet format for better performance

## Contributing

When contributing to this script:

1. Ensure all new features are documented in this runbook
2. Add appropriate error handling and logging
3. Include examples for new functionality
4. Update the troubleshooting section for new error conditions

## License

[Add your license information here]

---

> **Note**: This runbook is maintained alongside the `extractor.py` script. Please keep both in sync when making changes.
