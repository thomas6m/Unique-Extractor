# Test Data Generator

This Python script generates synthetic test datasets for users, products, and orders. It supports error injection for testing data validation and handling corrupt data. A YAML config file describing the datasets can also be generated.

## Features

- Generate CSV files for users and products
- Generate JSON file for orders
- Inject errors randomly or explicitly for testing
- Support duplicates and corrupt rows in test-case mode
- Config YAML file output describing the dataset schemas
- Customizable record counts and output locations
- Reproducible data via Faker seed

## Installation

Requires Python 3.7 or later.

Install dependencies:

```
pip install faker pyyaml
```

## Usage

```
python generate_test_data.py [options]
```

### Options

- `--output-dir`: Directory for output files (default: test_data)
- `--config-dir`: Directory for config file (default: <output-dir>/configs)
- `--inject-errors`: Enable random data errors
- `--test-case-mode`: Add corrupt rows and duplicates (implies error injection)
- `--file`: Files to generate (users, products, orders, config)
- `--users`: Number of user records (default: 1000)
- `--products`: Number of product records (default: 500)
- `--orders`: Number of order records (default: 500)
- `--faker-seed`: Seed for Faker (default: 42)
- `--verbose`: Enable debug logging

### Examples

Generate default datasets:

```
python generate_test_data.py
```

Generate users and products only:

```
python generate_test_data.py --file users products --users 1000 --products 200
```

Generate datasets with errors:

```
python generate_test_data.py --inject-errors
```

## Output

- `users.csv` — user dataset
- `products.csv` — product dataset
- `orders.json` — order dataset
- `configs/config.yaml` — configuration file

## License

MIT License
