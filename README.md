# Data Extractor

A powerful Python utility for extracting unique values from various data file formats with advanced filtering capabilities.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚀 Features

- **Multiple File Format Support**: CSV, JSON, YAML, and Parquet
- **Advanced Filtering**: Equality, inequality, numeric comparison, and regex matching
- **Flexible Output**: Multiple output formats and row arrangements
- **Interactive Mode**: User-friendly prompts when arguments are missing
- **Performance Monitoring**: Memory usage and execution time tracking
- **Robust Error Handling**: Comprehensive validation and error reporting
- **Configurable Logging**: File and console output with multiple log levels

## 📋 Prerequisites

- Python 3.7+
- Required packages (see [Installation](#installation))

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/data-extractor.git
   cd data-extractor
   ```

2. **Install dependencies**
   ```bash
   pip install polars pyyaml psutil
   ```

   Or using requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Quick Start

### Basic Usage
```bash
python extractor.py --input data.csv --output results.csv --unique-field email
```

### Advanced Usage with Filters
```bash
python extractor.py \
  --input data.json \
  --output results.yaml \
  --unique-field user_id \
  --filters "status=active,pending" "age>18" "name~^John" \
  --row-format multi \
  --output-format yaml
```

### Interactive Mode
```bash
python extractor.py
```

## 📚 Usage Guide

### Command Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `--input` | Input file path | - | Yes* |
| `--output` | Output file path | - | Yes* |
| `--unique-field` | Field to extract unique values from | - | Yes* |
| `--separator` | Separator for single-row output | `;` | No |
| `--column-name` | Custom column name for output | Same as unique-field | No |
| `--filters` | Filter expressions | None | No |
| `--row-format` | Output row format (`single`/`multi`) | `single` | No |
| `--output-format` | Output file format | `csv` | No |
| `--delimiter` | CSV input delimiter | `,` | No |
| `--log-level` | Logging level | `INFO` | No |

*Required unless using interactive mode

### Filter Syntax

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals (supports multiple values) | `status=active,pending` |
| `!=` | Not equals | `status!=inactive` |
| `>` | Greater than (numeric) | `age>18` |
| `<` | Less than (numeric) | `price<100` |
| `>=` | Greater than or equal | `score>=80` |
| `<=` | Less than or equal | `count<=50` |
| `~` | Regex match | `name~^John.*` |

### Supported File Formats

#### Input Formats
- **CSV**: Standard comma-separated values with configurable delimiter
- **JSON**: Standard JSON arrays/objects and NDJSON support
- **YAML**: Single and multi-document YAML files with nested structure flattening
- **Parquet**: Efficient columnar format with full schema preservation

#### Output Formats
- **Single Row**: All unique values in one row (concatenated)
- **Multi Row**: One row per unique value

## 💡 Examples

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

## 🔍 Interactive Mode

When required arguments are missing, the script automatically enters interactive mode:

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
```

## ⚡ Performance

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

## 📊 Logging

### Log Levels
- `DEBUG`: Detailed processing information
- `INFO`: General operation info (default)
- `WARNING`: Non-critical issues
- `ERROR`: Critical errors only

### Log Output
- **File**: `extractor.log` (always created)
- **Console**: Warnings and errors in interactive mode

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **File Not Found** | Check file path and ensure file exists |
| **Missing Columns** | Verify column names in your data file |
| **Invalid Filter Syntax** | Use proper operator syntax (e.g., `status=active`) |
| **Numeric Conversion Error** | Ensure numeric values when using comparison operators |
| **Unicode Errors** | Ensure input files are UTF-8 encoded |
| **Memory Issues** | Use `--log-level ERROR` and process smaller chunks |

### Debug Mode
```bash
python extractor.py --log-level DEBUG --input data.csv --output test.csv --unique-field id
```

### Getting Help
```bash
python extractor.py --help
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Extending the Script

Common extensions:
- Additional file format support
- Custom output transformations
- Database connectivity
- Parallel processing for very large files
- Custom filter operators

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For technical support or feature requests:
- Open an [issue](https://github.com/yourusername/data-extractor/issues)
- Check existing [discussions](https://github.com/yourusername/data-extractor/discussions)
- Review the [troubleshooting guide](#troubleshooting)

## 🏷️ Version History

- **v1.0.0** - Initial release with basic extraction functionality
- **v1.1.0** - Added interactive mode and advanced filtering
- **v1.2.0** - Multi-format support and performance improvements

---

⭐ **Star this repository if you find it useful!**
