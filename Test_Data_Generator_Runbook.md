# Runbook for Test Data Generator

## Purpose
This script generates synthetic test data sets for users, products, and orders, with options to inject errors for testing validation and handling corrupt data. It can also generate a YAML configuration file describing the generated data files.

## Setup Instructions

### Environment Setup
```bash
# Create project directory and Python virtual environment
mkdir -p TestData/python-env
python -m venv TestData/python-env
source TestData/python-env/bin/activate 
python -m pip install --upgrade pip
```

### Dependencies
```bash
# Create requirements file
tee TestData/requirements.txt <<EOF
faker
PyYAML
black
flake8
EOF

# Install dependencies
pip install -r TestData/requirements.txt
pip freeze > TestData/requirements-freeze.txt
```

### Script Setup
```bash
# Create the main script file
vi TestData/generate_test_data.py
```

---

## How to Run
```bash
python generate_test_data.py [options]
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir` | Directory where generated files will be saved | `test_data` |
| `--config-dir` | Directory to save YAML config file | `<output-dir>/configs` |
| `--faker-seed` | Seed for Faker and random for reproducibility | `42` |
| `--inject-errors` | Inject random data errors into the output | `False` |
| `--test-case-mode` | Adds explicit corrupt rows and duplicates (implies `--inject-errors`) | `False` |
| `--error-prob` | Probability of injecting errors into fields | `0.05` |
| `--duplicate-count` | Number of duplicate entries to add in test-case mode | `5` |
| `--verbose` | Enable verbose debug logging | `False` |
| `--file` | Files to generate. Choose any from: `users`, `products`, `orders`, `config` | All |
| `--users` | Number of user rows to generate | `1000` |
| `--products` | Number of product rows to generate | `500` |
| `--orders` | Number of order entries to generate | `500` |

## Example Commands

### Generate all files with defaults:
```bash
python generate_test_data.py
```

### Generate only users and products with 100 users and 200 products:
```bash
python generate_test_data.py --file users products --users 100 --products 200
```

### Generate data with errors injected (useful for testing error handling):
```bash
python generate_test_data.py --inject-errors
```

### Generate test-case mode with duplicates and explicit corrupt rows:
```bash
python generate_test_data.py --test-case-mode
```

### Verbose logging to debug output:
```bash
python generate_test_data.py --verbose
```

## Output Files

- **`users.csv`** — User data with fields like id, first_name, email, salary, hire_date, etc.
- **`products.csv`** — Product data including product_id, name, category, price, stock, etc.
- **`orders.json`** — Order entries linking users and products with quantities, prices, status, etc.
- **`configs/config.yaml`** — YAML configuration describing file schemas and keys.

## Troubleshooting

- Ensure you have installed the required Python packages.
- Use `--verbose` to get detailed logs.
- If files don't appear in expected folders, verify `--output-dir` and `--config-dir` paths.
- If you want reproducible data, use the same `--faker-seed`.

## File Structure

After running the setup and generation commands, your project structure should look like:

```
TestData/
├── python-env/              # Virtual environment
├── requirements.txt         # Project dependencies
├── requirements-freeze.txt  # Frozen dependency versions
├── generate_test_data.py    # Main script
└── test_data/              # Generated output (default)
    ├── users.csv
    ├── products.csv
    ├── orders.json
    └── configs/
        └── config.yaml
```
