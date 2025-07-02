# Test Data Generator - Operations Runbook

## Overview

The Test Data Generator is a Python utility designed to create realistic test datasets in multiple formats (CSV, JSON, YAML, Parquet) for testing data extraction and processing workflows. It generates synthetic data including users, products, events, logs, and configuration files.

## Prerequisites

### System Requirements
- Python 3.7+
- Required Python packages:
  - `polars` - For Parquet file generation
  - `pyyaml` - For YAML file processing
  - Standard library modules: `csv`, `json`, `random`, `string`, `argparse`, `pathlib`, `datetime`, `typing`, `uuid`

### Installation
```bash
# Install required dependencies
pip install polars pyyaml

# Make the script executable
chmod +x test_data_generator.py
```

## Usage

### Basic Usage

#### Generate All Test Files (Default)
```bash
python test_data_generator.py
```
This creates:
- `test_data/users.csv` (1000 users)
- `test_data/products.csv` (500 products)  
- `test_data/events.json` (300 events)
- `test_data/config.yaml` (100 services)
- `test_data/logs.parquet` (2000 log entries)
- `test_data/data_with_nulls.csv` (200 records with null values)
- `test_data/multi_delimited.csv` (150 records with various delimiters)
- Configuration files in `test_data/configs/`

#### Generate Specific File Types
```bash
# Generate only CSV files
python test_data_generator.py --file-type csv

# Generate only JSON files  
python test_data_generator.py --file-type json

# Generate only YAML files
python test_data_generator.py --file-type yaml

# Generate only Parquet files
python test_data_generator.py --file-type parquet
```

#### Custom Output Directory
```bash
python test_data_generator.py --output-dir /path/to/custom/directory
```

#### Skip Configuration Files
```bash
python test_data_generator.py --no-configs
```

## Generated Data Structure

### 1. Users CSV (`users.csv`)
**Columns:**
- `id` - Sequential user ID
- `first_name` - Random first name
- `last_name` - Random last name  
- `email` - Generated email address
- `phone` - US format phone number
- `age` - Age between 22-65
- `department` - One of 8 departments
- `status` - active/inactive/pending/suspended/archived
- `country` - One of 10 countries
- `salary` - Salary between $40,000-$150,000
- `hire_date` - Date within last 3 years
- `skills` - Semicolon-separated technology skills
- `projects` - Number of projects (1-10)
- `manager_email` - Manager's email (20% null)

### 2. Products CSV (`products.csv`)
**Columns:**
- `product_id` - Format: PROD-####
- `name` - Product name with variant
- `category` - Product category
- `price` - Price between $10.99-$2999.99
- `stock_quantity` - Stock level 0-1000
- `supplier_email` - Supplier contact
- `tags` - Semicolon-separated tags
- `launch_date` - Launch date within last 2 years
- `rating` - Rating 1.0-5.0
- `status` - Product status

### 3. Events JSON (`events.json`)
**NDJSON Format with fields:**
- `event_id` - UUID
- `timestamp` - Date within last 30 days
- `user_email` - User email
- `event_type` - login/logout/purchase/view/click/signup
- `source` - web/mobile/api/desktop
- `country` - Country code
- `session_id` - 8-character session ID
- `metadata` - Nested object with user_agent, ip_range, referrer

### 4. Config YAML (`config.yaml`)
**Structure:**
```yaml
version: "1.0"
generated_at: "2025-01-XX..."
services:
  - name: service-001
    type: web/api/database/cache/queue
    owner_email: owner@example.com
    environment: production/staging/development
    tags: [tag1, tag2]
    config:
      port: 3000-9000
      replicas: 1-5
      memory: "512Mi-4096Mi"
    dependencies: [tech1, tech2]
    status: active/inactive/etc
```

### 5. Logs Parquet (`logs.parquet`)
**Columns:**
- `timestamp` - Log timestamp (last 7 days)
- `level` - INFO/DEBUG/WARNING/ERROR/CRITICAL
- `service` - Service name (service-01 to service-20)
- `user_email` - Associated user (30% null)
- `message` - Log message
- `source_file` - Source Python file
- `line_number` - Line number 1-500
- `execution_time_ms` - Execution time 1-5000ms
- `memory_usage_mb` - Memory usage 10-512MB

### 6. Data with Nulls CSV (`data_with_nulls.csv`)
**Purpose:** Testing null value handling
- 15% null emails
- 10% null departments  
- 50% null optional fields

### 7. Multi-Delimited CSV (`multi_delimited.csv`)
**Purpose:** Testing different delimiter parsing
- `skills_semicolon` - Skills separated by `;`
- `tags_comma` - Tags separated by `,`
- `contacts_pipe` - Contacts separated by `|`
- `categories_space` - Categories separated by ` `

## Configuration Files

The tool generates sample configuration files in `test_data/configs/`:

### 1. `extract_emails.yaml`
```yaml
input_file: test_data/users.csv
output_file: results/unique_emails.csv
unique_field: email
filters:
  - [status, =, [active]]
  - [age, ">=", [25]]
drop_na: true
row_format: multi
output_format: csv
```

### 2. `extract_skills.yaml`
```yaml
input_file: test_data/users.csv
output_file: results/unique_skills.json
unique_field: skills
separator: ";"
row_format: multi
output_format: json
filters:
  - [department, =, [Engineering, Technology]]
```

### 3. `extract_departments.yaml`
```yaml
input_file: test_data/users.csv
output_file: results/departments.yaml
unique_field: department
row_format: single
output_format: yaml
separator: " | "
```

### 4. `extract_event_types.yaml`
```yaml
input_file: test_data/events.json
output_file: results/event_types.csv
unique_field: event_type
filters:
  - [source, =, [web, mobile]]
row_format: multi
```

## Data Pools and Randomization

The generator uses predefined data pools to ensure realistic and consistent test data:

- **Names:** 10 first names, 10 last names
- **Domains:** 6 email domains
- **Departments:** 8 departments
- **Countries:** 10 countries
- **Technologies:** 10 technology skills
- **Categories:** 10 product categories

## Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
# Error: ModuleNotFoundError: No module named 'polars'
pip install polars pyyaml
```

#### Permission Errors
```bash
# Error: Permission denied when creating directories
chmod +w /path/to/output/directory
# Or use --output-dir with writable location
python test_data_generator.py --output-dir ~/test_data
```

#### Memory Issues with Large Files
```bash
# For very large datasets, monitor memory usage
# Parquet files are most memory-intensive
# Consider reducing row counts for large datasets
```

### Validation

#### Verify Generated Files
```bash
# Check file sizes
ls -la test_data/

# Verify CSV structure
head -5 test_data/users.csv

# Check JSON format
head -3 test_data/events.json | jq '.'

# Verify Parquet file
python -c "import polars as pl; df = pl.read_parquet('test_data/logs.parquet'); print(df.shape)"
```

#### Data Quality Checks
```bash
# Check for expected null values
python -c "
import pandas as pd
df = pd.read_csv('test_data/data_with_nulls.csv')
print('Null percentages:')
print(df.isnull().sum() / len(df) * 100)
"
```

## Performance Considerations

### File Size Estimates
- **users.csv (1000 rows):** ~200KB
- **products.csv (500 rows):** ~100KB
- **events.json (300 rows):** ~150KB
- **config.yaml (100 services):** ~50KB
- **logs.parquet (2000 rows):** ~300KB
- **data_with_nulls.csv (200 rows):** ~30KB
- **multi_delimited.csv (150 rows):** ~40KB

### Generation Time
- **All files:** ~2-5 seconds on modern hardware
- **Large datasets (10K+ rows):** Scale linearly

## Integration with Data Extractor

The generated test data is designed to work with a data extraction tool. Example commands:

```bash
# Extract unique emails from users
python extractor.py --config test_data/configs/extract_emails.yaml

# Extract skills with custom parameters
python extractor.py --input test_data/users.csv --output results/emails.csv --unique-field email --filters 'status=active'

# Extract multi-delimited fields
python extractor.py --input test_data/multi_delimited.csv --output results/skills.csv --unique-field skills_semicolon --separator ';' --row-format multi
```

## Customization

### Extending Data Pools
To add new data options, modify the `__init__` method:

```python
self.new_field_options = ["option1", "option2", "option3"]
```

### Custom File Generators
Add new methods following the pattern:
```python
def generate_custom_format(self, num_rows: int = 100) -> str:
    filename = self.output_dir / "custom.ext"
    # Generation logic here
    print(f"✅ Generated {filename} with {num_rows} rows")
    return str(filename)
```

## Maintenance

### Regular Tasks
- Monitor disk space in output directories
- Update data pools periodically for realism
- Validate generated data quality
- Update dependencies: `pip install --upgrade polars pyyaml`

### Monitoring
- Check for Python version compatibility
- Verify file permissions
- Monitor generation performance
- Validate file formats after generation

## Security Considerations

- Generated data is synthetic and safe for testing
- Email addresses use common domains but are not real
- No sensitive or personal data is included
- Safe for use in development/testing environments
