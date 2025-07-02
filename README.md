# Data Extractor Tool

A robust command-line tool for extracting unique values from tabular data files with flexible filtering and output options.

## Features

- **Multiple file formats**: CSV, JSON, YAML, Parquet
- **Flexible filtering**: Support for various operators (=, !=, >, <, >=, <=, ~)
- **Multi-value field handling**: Split delimited values and extract unique items
- **Multiple output formats**: CSV, JSON, YAML, Parquet
- **Configuration options**: Command-line arguments or YAML config file
- **Memory monitoring**: Built-in memory usage tracking
- **Comprehensive logging**: Detailed execution logs
- **Dry run mode**: Preview results without writing files

## Installation

### Requirements

```bash
pip install polars pyyaml psutil
```

### Dependencies

- `polars` - Fast DataFrame processing
- `pyyaml` - YAML file handling
- `psutil` - Memory monitoring
- `argparse` - Command-line interface (built-in)
- `logging` - Execution logging (built-in)

## Usage

### Command Line Interface

#### Basic Usage

```bash
python extractor.py --input data.csv --output results.csv --unique-field email
```

#### Advanced Usage with Filters

```bash
python extractor.py \
  --input data/input.csv \
  --output results/unique_emails.csv \
  --unique-field email \
  --filters "status=active" "age>=18" \
  --separator ";" \
  --row-format single \
  --output-format csv \
  --drop-na
```

#### Using Configuration File

```bash
python extractor.py --config config.yaml
```

### Configuration File

Create a `config.yaml` file for reusable configurations:

```yaml
input_file: "data/input.csv"
output_file: "results/unique_emails.csv"
unique_field: "email"
filters:
  - ["status", "=", ["active"]]
  - ["age", ">=", ["18"]]
separator: ";"
row_format: "single"      # or "multi"
output_format: "csv"      # csv, json, yaml, parquet
delimiter: ","            # CSV delimiter for input file
drop_na: true             # drop rows where field is null
dry_run: false            # preview mode without writing files
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input` | Input file path | Required |
| `--output` | Output file path | Required |
| `--unique-field` | Field to extract unique values from | Required |
| `--config` | YAML configuration file path | None |
| `--filters` | Filter expressions (e.g., "status=active") | None |
| `--separator` | Delimiter for multi-value fields | ";" |
| `--row-format` | Output format: "single" or "multi" | "single" |
| `--output-format` | Output file format: csv, json, yaml, parquet | "csv" |
| `--delimiter` | CSV input delimiter | "," |
| `--column-name` | Custom output column name | None |
| `--drop-na` | Drop null values | False |
| `--dry-run` | Preview without writing files | False |
| `--print-config-template` | Print sample YAML config | - |

## Filtering

The tool supports various filter operations:

### Filter Operators

- `=` - Exact match
- `!=` - Not equal
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `~` - Regex contains

### Filter Examples

```bash
# Single filter
--filters "status=active"

# Multiple filters (AND logic)
--filters "status=active" "age>=18" "department!=HR"

# Regex filter
--filters "email~@company\.com$"
```

## Output Formats

### Row Formats

- **single**: All unique values joined as one string in a single row
- **multi**: Each unique value on its own row

### File Formats

- **CSV**: Comma-separated values
- **JSON**: JavaScript Object Notation
- **YAML**: YAML Ain't Markup Language
- **Parquet**: Columnar storage format

## Multi-Value Field Processing

When dealing with fields containing multiple values separated by a delimiter:

```csv
id,tags
1,"python;data;analysis"
2,"web;javascript;react"
```

Using `--separator ";"` and `--row-format multi` will extract:
- python
- data
- analysis
- web
- javascript
- react

## Examples

### Extract Unique Email Addresses

```bash
python extractor.py \
  --input users.csv \
  --output unique_emails.csv \
  --unique-field email \
  --filters "status=active" \
  --drop-na
```

### Extract Tags from Multi-Value Field

```bash
python extractor.py \
  --input posts.json \
  --output unique_tags.yaml \
  --unique-field tags \
  --separator "," \
  --row-format multi \
  --output-format yaml
```

### Dry Run with Preview

```bash
python extractor.py \
  --input data.csv \
  --output preview.csv \
  --unique-field category \
  --dry-run
```

## Architecture Overview

### Core Components

1. **Configuration Management**: `ExtractorConfig` dataclass for parameter handling
2. **File I/O**: Support for multiple input/output formats using Polars
3. **Data Processing**: Efficient DataFrame operations with memory monitoring
4. **Filtering Engine**: `FilterParser` and `FilterApplier` for flexible data filtering
5. **Logging System**: Comprehensive execution tracking and error handling

### Data Flow

1. **Input Validation**: Verify file existence and format
2. **Data Loading**: Read data using appropriate Polars reader
3. **Data Flattening**: Convert nested structures to tabular format
4. **Filter Application**: Apply user-defined filters
5. **Unique Extraction**: Extract and sort unique values
6. **Output Generation**: Save results in specified format

## Error Handling

The tool provides comprehensive error handling for:

- Invalid file paths or formats
- Memory limitations
- Malformed filter expressions
- Data processing errors
- Output writing failures

## Logging

Execution logs are automatically saved to the `logs/` directory with timestamps and include:

- Configuration details
- Processing statistics
- Memory usage
- Error messages
- Execution time

## Performance

- Built on Polars for high-performance data processing
- Memory usage monitoring to prevent system overload
- Lazy evaluation for efficient large dataset handling
- Optimized for both small and large datasets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License



---

**Generate Config Template**
```bash
python extractor.py --print-config-template
```

This will output a sample YAML configuration file that you can customize for your needs.
