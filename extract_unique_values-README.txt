# Data Extractor Script Documentation

## Overview

The Data Extractor is a powerful Python utility designed to extract unique values from various data file formats with advanced filtering capabilities. It supports CSV, JSON, YAML, and Parquet files, offering both command-line and interactive modes for maximum flexibility.

## Features

- **Multiple File Format Support**: CSV, JSON, YAML, Parquet
- **Advanced Filtering**: Support for equality, inequality, numeric comparison, and regex matching
- **Flexible Output**: Multiple output formats and row arrangements
- **Interactive Mode**: User-friendly prompts when arguments are missing
- **Performance Monitoring**: Memory usage and execution time tracking
- **Robust Error Handling**: Comprehensive validation and error reporting
- **Logging**: Configurable logging with file and console output

## Installation

### Prerequisites

```bash
pip install polars pyyaml psutil
```

### Required Python Version
- Python 3.7+

## Usage

### Command Line Interface

#### Basic Usage
```bash
python extractor.py --input data.csv --output results.csv --unique-field email
```

#### Advanced Usage with Filters
```bash
python extractor.py \
  --input data.json \
  --output results.yaml \
  --unique-field user_id \
  --filters "status=active,pending" "age>18" "name~^John" \
  --row-format multi \
  --output-format yaml
```

#### Interactive Mode
```bash
python extractor.py
```
*Launches interactive mode when required arguments are missing*

### Command Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `--input` | Input file path | - | Yes* |
| `--output` | Output file path | - | Yes* |
| `--unique-field` | Field to extract unique values from | - | Yes* |
| `--separator` | Separator for single-row output | `;` | No |
| `--column-name` | Custom column name for output | Same as unique-field | No |
| `--filters` | Filter expressions (see Filter Syntax) | None | No |
| `--row-format` | Output row format (`single`/`multi`) | `single` | No |
| `--output-format` | Output file format | `csv` | No |
| `--delimiter` | CSV input delimiter | `,` | No |
| `--log-level` | Logging level | `INFO` | No |

*Required unless using interactive mode

## Filter Syntax

### Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals (supports multiple values) | `status=active,pending` |
| `!=` | Not equals | `status!=inactive` |
| `>` | Greater than (numeric) | `age>18` |
| `<` | Less than (numeric) | `price<100` |
| `>=` | Greater than or equal | `score>=80` |
| `<=` | Less than or equal | `count<=50` |
| `~` | Regex match | `name~^John.*` |

### Filter Examples

```bash
# Single value equality
--filters "country=USA"

# Multiple values (OR condition)
--filters "status=active,pending,review"

# Numeric comparison
--filters "age>21" "salary>=50000"

# Regex matching
--filters "email~.*@company\.com$"

# Complex combination
--filters "department=engineering,sales" "level>=senior" "active=true"
```

## Supported File Formats

### Input Formats

#### CSV
- Standard comma-separated values
- Configurable delimiter
- Automatic schema inference
- Handles ragged lines gracefully

```bash
python extractor.py --input data.csv --delimiter ";" --unique-field email
```

#### JSON
- Standard JSON arrays/objects
- NDJSON (newline-delimited JSON) support
- Automatic format detection

#### YAML
- Single and multi-document YAML files
- Nested structure flattening with dot notation
- List handling with indexed keys

#### Parquet
- Efficient columnar format
- Full schema preservation
- High-performance reading

### Output Formats

#### Single Row Format (`--row-format single`)
Creates one row with all unique values concatenated:

```csv
filters,unique_emails
"status=active",john@example.com;jane@example.com;bob@example.com
```

#### Multi Row Format (`--row-format multi`)
Creates one row per unique value:

```csv
unique_emails
john@example.com
jane@example.com
bob@example.com
```

## Configuration Class

The script uses a configuration dataclass for internal organization:

```python
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
    filters: List[Tuple[str, str, List[str]]] = None
```

## Special Features

### Contact IDs Processing
Special handling for comma-separated contact ID fields:

```bash
python extractor.py --input contacts.csv --unique-field contact_ids --output unique_contacts.csv
```

This will:
1. Split comma-separated values in the `contact_ids` field
2. Extract unique individual contact IDs
3. Remove duplicates and empty values

### Nested Data Flattening
YAML and JSON nested structures are automatically flattened:

```yaml
# Input YAML
user:
  profile:
    name: "John Doe"
    details:
      age: 30
      city: "New York"
```

Becomes:
```
user.profile.name: "John Doe"
user.profile.details.age: 30
user.profile.details.city: "New York"
```

## Interactive Mode

When required arguments are missing, the script enters interactive mode:

```
⚡ Interactive mode enabled...
Enter input file path: data.csv

📌 Available fields (5): name, email, age, department, status

Field name (or 'done' to finish): status
🔹 Unique values for 'status' (3): active, inactive, pending
Operator ['=', '!=', '>', '<', '>=', '<=', '~'] (default '='): =
Enter comma-separated value(s): active,pending
✅ Added filter: status = active, pending

Field name (or 'done' to finish): done

🎯 Available fields: name, email, age, department, status
Field to extract unique values from: email

Separator for single-row output (default: ;): 
Column name (default: email): 
Row format (single/multi) [default: single]: 
Output format (csv/json/yaml/parquet) [default: csv]: 
Output file path: unique_emails.csv
```

## Error Handling

### Common Errors and Solutions

#### File Not Found
```
❌ File does not exist: data.csv
```
**Solution**: Check file path and ensure file exists

#### Missing Columns
```
❌ Missing columns in input file: {'status', 'department'}
```
**Solution**: Verify column names in your data file

#### Invalid Filter Syntax
```
⚠️ Skipping invalid filter 'status': Invalid filter format
```
**Solution**: Use proper operator syntax (e.g., `status=active`)

#### Numeric Conversion Error
```
❌ Cannot convert 'abc' to number for comparison
```
**Solution**: Ensure numeric values when using `>`, `<`, `>=`, `<=` operators

## Performance Considerations

### Memory Usage
- Uses Polars LazyFrames for memory-efficient processing
- Suitable for large datasets (tested with files up to several GB)
- Memory usage reported at completion

### File Size Recommendations
- **CSV**: Up to 1GB+ (depends on available RAM)
- **JSON**: Up to 500MB (due to parsing overhead)
- **Parquet**: Up to 2GB+ (most efficient format)
- **YAML**: Up to 100MB (due to parsing complexity)

### Performance Tips
1. Use Parquet format for large datasets
2. Apply filters to reduce data early
3. Use `--log-level ERROR` for better performance in batch processing
4. Consider splitting very large files if memory issues occur

## Logging

### Log Levels
- `DEBUG`: Detailed processing information
- `INFO`: General operation info (default)
- `WARNING`: Non-critical issues
- `ERROR`: Critical errors only

### Log Output
- File: `extractor.log` (always created)
- Console: Warnings and errors in interactive mode

### Example Log Entry
```
2024-01-15 10:30:15 - INFO - Reading CSV file: /path/to/data.csv (45.2 MB)
2024-01-15 10:30:18 - INFO - Applied filter: status = ['active', 'pending']
2024-01-15 10:30:19 - INFO - Saved 1,234 unique values to /path/to/output.csv
```

## Examples

### Example 1: Basic Email Extraction
```bash
python extractor.py \
  --input customer_data.csv \
  --output unique_emails.csv \
  --unique-field email \
  --filters "status=active"
```

### Example 2: Multi-format Processing
```bash
python extractor.py \
  --input users.json \
  --output active_users.yaml \
  --unique-field user_id \
  --filters "account_type=premium,enterprise" "last_login>=2024-01-01" \
  --row-format multi \
  --output-format yaml
```

### Example 3: Complex Filtering
```bash
python extractor.py \
  --input sales_data.parquet \
  --output filtered_customers.json \
  --unique-field customer_id \
  --filters "region=north,south" "revenue>10000" "customer_name~.*Corp$" \
  --output-format json
```

### Example 4: Contact ID Processing
```bash
python extractor.py \
  --input campaign_data.csv \
  --output unique_contacts.csv \
  --unique-field contact_ids \
  --filters "campaign_status=completed" "send_date>=2024-01-01"
```

## API Reference

### Core Functions

#### `read_input_file(filepath: Path, delimiter: str) -> pl.DataFrame`
Reads input file based on extension.

**Parameters:**
- `filepath`: Path to input file
- `delimiter`: CSV delimiter (ignored for other formats)

**Returns:** Polars DataFrame

#### `extract_unique_values(config: ExtractorConfig) -> pl.Series`
Main extraction logic with filtering.

**Parameters:**
- `config`: ExtractorConfig object

**Returns:** Polars Series of unique values

#### `save_output(series: pl.Series, config: ExtractorConfig) -> None`
Saves output in specified format.

**Parameters:**
- `series`: Unique values series
- `config`: Configuration object

### Classes

#### `FileReader`
Static methods for reading different file formats.

#### `FilterParser`
Handles parsing and validation of filter expressions.

#### `FilterApplier`
Applies filters to LazyFrames.

#### `InteractivePrompts`
Manages interactive user input.

## Troubleshooting

### Common Issues

1. **Unicode Errors**: Ensure input files are UTF-8 encoded
2. **Memory Issues**: Use `--log-level ERROR` and process smaller chunks
3. **Regex Errors**: Escape special characters in regex patterns
4. **CSV Parsing**: Adjust `--delimiter` for non-standard CSV files
5. **YAML Complex Structures**: Nested lists may need preprocessing

### Debug Mode
```bash
python extractor.py --log-level DEBUG --input data.csv --output test.csv --unique-field id
```

### Getting Help
```bash
python extractor.py --help
```

## License and Contributing

This script is provided as-is for data processing tasks. Feel free to modify and extend based on your needs.

### Extending the Script

Common extensions:
- Additional file format support
- Custom output transformations
- Database connectivity
- Parallel processing for very large files
- Custom filter operators

---

*For technical support or feature requests, please refer to your internal documentation or contact the development team.*
