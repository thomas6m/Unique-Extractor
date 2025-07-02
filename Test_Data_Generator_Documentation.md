# Test Data Generator Documentation

Test Data Generator tool is for generating synthetic test data (users, products, orders) in CSV/JSON formats, with optional errors for validation testing.

## CLI Options

```
usage: generate_test_data.py [-h] [--output-dir OUTPUT_DIR] [--config-dir CONFIG_DIR]
                             [--faker-seed FAKER_SEED] [--inject-errors] [--test-case-mode]
                             [--error-prob ERROR_PROB] [--duplicate-count DUPLICATE_COUNT]
                             [--verbose] [--file {users,products,orders,config} [file ...]]
                             [--users USERS] [--products PRODUCTS] [--orders ORDERS]
```

Generate test data sets for users, products, and orders with optional error injection.

## 🔧 Option Descriptions

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message and exit. |
| `--output-dir OUTPUT_DIR` | Where to save generated data files.<br>**Default:** `test_data`.<br>**Example:** `--output-dir ./mydata` |
| `--config-dir CONFIG_DIR` | Where to save the config YAML file.<br>**Default:** `<output-dir>/configs`.<br>**Example:** `--config-dir ./configs` |
| `--faker-seed FAKER_SEED` | Seed value for the Faker library and random to ensure repeatable output.<br>**Default:** `42`.<br>Set a different seed for varied data each time. |
| `--inject-errors` | Enable random data errors (e.g., bad emails, negative values).<br>Useful for testing how your app handles bad data. |
| `--test-case-mode` | Adds explicit corrupt rows (e.g., empty fields, strings in numeric columns) and duplicates.<br>⚠️ This implies `--inject-errors`. |
| `--error-prob ERROR_PROB` | How likely each field will be corrupted.<br>**Range:** 0 to 1. **Default:** 0.05 (5%). |
| `--duplicate-count DUPLICATE_COUNT` | How many duplicate IDs to add if `--test-case-mode` is on.<br>**Default:** 5. |
| `--verbose` | Turn on debug logging. Prints more info while running (e.g., when errors are injected). |
| `--file {users,products,orders,config} [...]` | Select which files to generate. By default, all are created.<br>**Example:** `--file users orders`<br>**Valid values:** users, products, orders, config |
| `--users USERS` | Number of user rows to generate (**default:** 1000). |
| `--products PRODUCTS` | Number of product rows to generate (**default:** 500). |
| `--orders ORDERS` | Number of order entries to generate (**default:** 500). |

## 💡 Examples

### Basic Example – Generate all default data
```bash
python TestDataGenerator.py
```

### Generate only users and products, with 100 each
```bash
python TestDataGenerator.py --file users products --users 100 --products 100
```

### Generate bad data for testing
```bash
python TestDataGenerator.py --test-case-mode
```

### Save output to custom directory
```bash
python TestDataGenerator.py --output-dir ./generated_data --config-dir ./generated_data/configs
```

### Enable debug output (see what's being injected)
```bash
python TestDataGenerator.py --verbose --inject-errors
```

## Sample CLI Command

```bash
python generate_test_data.py --output-dir ./sample_data --users 10 --products 5 --orders 5 --inject-errors --test-case-mode --verbose
```

## Sample Output Files

### 1. ./sample_data/users.csv

```csv
id,first_name,last_name,email,phone,age,department,status,country,salary,hire_date,skills,projects,manager_email
USR-0001,John,Doe,john.doe@gmail.com,+1-234-567-8901,29,Engineering,active,USA,70000,2021-05-14,Python;JavaScript,3,jane.smith@company.com
USR-0002,Jane,Smith,malformed-email@@,+1-987-654-3210,-1,Marketing,inactive,Canada,N/A,2023-99-99,Java;React,1,
...
CORRUPT,,,,???,abc,old,,,,none,invalid-date,,NaN,
```

- 10 user rows (some with injected errors like malformed emails, invalid ages, or salaries)
- One explicit corrupt row at the end (due to test-case-mode)

### 2. ./sample_data/products.csv

```csv
product_id,name,category,price,stock_quantity,supplier_email,tags,launch_date,rating,status
PROD-0001,Laptop Pro X,Technology,1299.99,50,supplier@example.org,Python;AWS,2022-08-10,4.5,active
PROD-0002,Monitor 4K Elite,Science,free,-100,malformed-email@@,Docker;Kubernetes,00-00-0000,10,archived
...
CORRUPT,,,free,many,???,,invalid-date,bad,
```

- 5 product rows, some with error injection (negative stock, malformed emails, invalid dates)
- Explicit corrupt row appended

### 3. ./sample_data/orders.json

```json
[
  {
    "order_id": "ORD-00001",
    "user_id": "USR-0005",
    "product_id": "PROD-0003",
    "quantity": 2,
    "price_per_unit": 499.99,
    "order_date": "2023-04-20",
    "status": "active"
  },
  {
    "order_id": "ORD-00002",
    "user_id": "USR-0001",
    "product_id": "PROD-0001",
    "quantity": "many",
    "price_per_unit": "cheap",
    "order_date": "invalid-date",
    "status": ""
  }
]
```

- 5 order entries (some fields with injected errors)
- Includes one explicit corrupt order entry at the end (because of test-case-mode)

### 4. ./sample_data/configs/config.yaml

```yaml
users:
  fields:
  - id
  - first_name
  - last_name
  - email
  - phone
  - age
  - department
  - status
  - country
  - salary
  - hire_date
  - skills
  - projects
  - manager_email
  file: users.csv
  delimiter: ","
  primary_key: id
products:
  fields:
  - product_id
  - name
  - category
  - price
  - stock_quantity
  - supplier_email
  - tags
  - launch_date
  - rating
  - status
  file: products.csv
  delimiter: ","
  primary_key: product_id
orders:
  fields:
  - order_id
  - user_id
  - product_id
  - quantity
  - price_per_unit
  - order_date
  - status
  file: orders.json
  format: json
  primary_key: order_id
```
