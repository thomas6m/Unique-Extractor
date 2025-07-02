# Data Extractor Tool

A powerful command-line data processing tool for extracting unique values from structured datasets with advanced filtering and multiple output format support.

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/extractor/graphs/commit-activity)

## 🚀 Features

- **Multi-format Support**: Read from CSV, JSON, YAML, and Parquet files
- **Advanced Filtering**: Apply complex filters with multiple operators (`=`, `!=`, `>`, `<`, `>=`, `<=`, `~`)
- **Flexible Output**: Export to CSV, JSON, YAML, or Parquet formats
- **Data Cleaning**: Handle multi-value fields, whitespace cleanup, and null removal
- **Performance Monitoring**: Built-in memory and execution time tracking
- **Comprehensive Logging**: Detailed logs with configurable levels
- **Dry Run Mode**: Test operations without modifying files

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/yourusername/extractor.git
cd extractor
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Python Packages

```
pandas>=1.3.0
pyyaml>=5.4.0
pyarrow>=4.0.0  # For Parquet support
```

## 🛠 Quick Start

### Basic Usage

Extract unique email addresses from a CSV file:

```bash
python extractor.py --input data.csv --output emails.csv --unique-field email
```

### Advanced Example

Extract unique user IDs with filtering and custom output format:

```bash
python extractor.py \
  --input users.json \
  --output active_users.yaml \
  --unique-field user_id \
  --filters "status=active" "age>=18" "country!=banned" \
  --drop-na \
  --output-format yaml \
  --log-level DEBUG
```

## 📖 Usage

### Command Syntax

```bash
python extractor.py [OPTIONS]
```

### Required Arguments

| Argument | Description |
|----------|-------------|
| `--input` | Path to input file (CSV, JSON, YAML, Parquet) |
| `--output` | Path to save the output file |
| `--unique-field` | Column name to extract unique values from |

### Optional Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--filters` | Apply data filters (see [Filtering](#filtering)) | None |
| `--delimiter` | CSV delimiter character | `,` |
| `--separator` | Multi-value field separator | `;` |
| `--column-name` | Output column name | Same as `unique-field` |
| `--row-format` | Output format: `single` or `multi` | `single` |
| `--output-format` | Output file format: `csv`, `json`, `yaml`, `parquet` | `csv` |
| `--log-level` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |
| `--drop-na` | Exclude null/empty values | `False` |
| `--dry-run` | Preview operations without saving | `False` |

## 🔍 Filtering

### Filter Syntax

```bash
--filters "column_name operator value"
```

### Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `--filters "status=active"` |
| `!=` | Not equals | `--filters "status!=inactive"` |
| `>` | Greater than | `--filters "age>21"` |
| `<` | Less than | `--filters "score<100"` |
| `>=` | Greater or equal | `--filters "rating>=4.0"` |
| `<=` | Less or equal | `--filters "price<=50.00"` |
| `~` | Regex match | `--filters "email~@company\.com"` |

### Multiple Filters

Apply multiple conditions:

```bash
--filters "age>=18" "status=active" "country=US,CA,UK"
```

### Multiple Values

Use comma-separated values for `=` and `!=`:

```bash
--filters "department=sales,marketing,support"
```

## 📁 Supported File Formats

### Input Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| CSV | `.csv` | Configurable delimiter |
| JSON | `.json` | Arrays and NDJSON supported |
| YAML | `.yaml`, `.yml` | Automatically flattened |
| Parquet | `.parquet` | High-performance columnar format |

### Output Examples

**CSV Output:**
```csv
email
user1@example.com
user2@example.com
```

**JSON Output:**
```json
[
  {"email": "user1@example.com"},
  {"email": "user2@example.com"}
]
```

**YAML Output:**
```yaml
- email: user1@example.com
- email: user2@example.com
```

## 📊 Examples

### Example 1: Customer Email Extraction

```bash
python extractor.py \
  --input customers.csv \
  --output customer_emails.csv \
  --unique-field email \
  --filters "subscription_status=active" \
  --drop-na
```

### Example 2: Product ID Analysis

```bash
python extractor.py \
  --input inventory.json \
  --output product_ids.txt \
  --unique-field product_id \
  --filters "category=electronics" "price>100" \
  --row-format multi \
  --output-format csv
```

### Example 3: User Analytics with Dry Run

```bash
python extractor.py \
  --input user_data.parquet \
  --output user_segments.yaml \
  --unique-field user_segment \
  --filters "last_login>=2024-01-01" "status!=suspended" \
  --output-format yaml \
  --dry-run \
  --log-level DEBUG
```

## 📝 Logging

Logs are automatically saved to `logs/extractor.log` with timestamps and detailed information:

```
2024-01-15 10:30:45 INFO - Loading input file: data.csv
2024-01-15 10:30:45 INFO - Applying filters: ['status=active']
2024-01-15 10:30:46 INFO - Extracted 1,234 unique values
2024-01-15 10:30:46 INFO - Saved output to: results.csv
```

## 🚨 Troubleshooting

### Common Issues

| Error | Solution |
|-------|----------|
| `FileNotFoundError` | Verify input file path exists |
| `Field not found` | Check column name spelling and case |
| `Unsupported format` | Use supported file extensions |
| `Memory error` | Process smaller chunks or use Parquet format |
| `Permission denied` | Check file/directory permissions |

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
python extractor.py --log-level DEBUG [other options]
```

## 🏗 Project Structure

```
extractor/
├── extractor.py          # Main script
├── requirements.txt      # Python dependencies
├── logs/                # Log files directory
│   └── extractor.log
├── tests/               # Unit tests
│   ├── test_extractor.py
│   └── sample_data/
├── docs/                # Documentation
│   └── runbook.md
└── README.md           # This file
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run with coverage:

```bash
python -m pytest tests/ --cov=extractor
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/yourusername/extractor.git
cd extractor
pip install -r requirements-dev.txt
pre-commit install
```

### Code Style

We use `black` for code formatting and `flake8` for linting:

```bash
black extractor.py
flake8 extractor.py
```

## 📈 Performance

### Benchmarks

| File Size | Records | Processing Time | Memory Usage |
|-----------|---------|----------------|--------------|
| 1 MB | 10K | 0.5s | 15 MB |
| 10 MB | 100K | 2.1s | 45 MB |
| 100 MB | 1M | 12.3s | 180 MB |

### Optimization Tips

- Use Parquet format for large datasets
- Apply filters early to reduce processing load
- Use `--drop-na` to exclude empty values
- Monitor memory usage with built-in reporting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pandas](https://pandas.pydata.org/) for data processing
- [PyArrow](https://arrow.apache.org/docs/python/) for Parquet support
- [PyYAML](https://pyyaml.org/) for YAML handling

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/extractor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/extractor/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/extractor/wiki)

---

⭐ **Star this repository if you find it useful!**
