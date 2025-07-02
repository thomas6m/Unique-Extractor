# Runbook for Test Data Generator

## Purpose

This script generates synthetic test data sets for users, products, and orders, with options to inject errors for testing validation and handling corrupt data. It can also generate a YAML configuration file describing the generated data files.

## Prerequisites

- Python 3.7+
- Install dependencies: `faker`, `pyyaml`

```bash
pip install faker pyyaml
```

## How to Run

```
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
```
python generate_test_data.py
```

### Generate only users and products with 100 users and 200 products:
```
python generate_test_data.py --file users products --users 100 --products 200
```

### Generate data with errors injected (useful for testing error handling):
```
python generate_test_data.py --inject-errors
```

### Generate test-case mode with duplicates and explicit corrupt rows:
```
python generate_test_data.py --test-case-mode
```

### Verbose logging to debug output:
```
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
