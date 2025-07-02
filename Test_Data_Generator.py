#!/usr/bin/env python3

import csv
import json
import yaml
import random
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Any, Optional, Dict
import sys
from faker import Faker

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class TestDataGenerator:
    USER_FIELDS = [
        'id', 'first_name', 'last_name', 'email', 'phone', 'age',
        'department', 'status', 'country', 'salary', 'hire_date',
        'skills', 'projects', 'manager_email'
    ]

    PRODUCT_FIELDS = [
        'product_id', 'name', 'category', 'price', 'stock_quantity',
        'supplier_email', 'tags', 'launch_date', 'rating', 'status'
    ]

    ORDER_FIELDS = [
        'order_id', 'user_id', 'product_id', 'quantity', 'price_per_unit',
        'order_date', 'status'
    ]

    VALID_FILETYPES = {"users", "products", "orders", "config"}

    MALFORMED_EMAILS = [
        "malformed-email@@", "invalid..email@example.com",
        "missing-at-sign.com", "wrong@domain@domain.com",
        "spaces in@email.com", "trailingdot.@example.com",
    ]

    INVALID_DATES = [
        "00-00-0000", "99-99-9999", "2023/99/99", "2023-13-01",
        "2023-00-10", "2023-02-30", "31-04-2022"
    ]

    def __init__(
        self,
        output_dir: str = "test_data",
        config_dir: Optional[str] = None,
        faker_seed: int = 42,
        inject_errors: bool = False,
        test_case_mode: bool = False,
        error_prob: float = 0.05,
        duplicate_count: int = 5,
        verbose: bool = False,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.config_dir = Path(config_dir) if config_dir else self.output_dir / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.inject_errors = inject_errors
        self.test_case_mode = test_case_mode
        self.error_prob = error_prob
        self.duplicate_count = duplicate_count

        self.faker = Faker()
        self.faker.seed_instance(faker_seed)
        random.seed(faker_seed)

        self.first_names = [self.faker.first_name() for _ in range(50)]
        self.last_names = [self.faker.last_name() for _ in range(50)]
        self.domains = ["gmail.com", "yahoo.com", "hotmail.com", "company.com", "example.org", "test.net"]
        self.departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations", "Legal", "Support"]
        self.statuses = ["active", "inactive", "pending", "suspended", "archived"]
        self.countries = ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia", "Brazil", "India", "China"]
        self.technologies = ["Python", "JavaScript", "Java", "C++", "React", "Node.js", "Docker", "Kubernetes", "AWS", "MongoDB"]
        self.categories = ["Technology", "Business", "Science", "Art", "Sports", "Music", "Travel", "Food", "Health", "Education"]

        if verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled.")

    def _maybe_inject_error(self, value: Any, field_name: str) -> Any:
        if not self.inject_errors:
            return value

        if random.random() > self.error_prob:
            return value

        errors = {
            'email': random.choice(self.MALFORMED_EMAILS),
            'age': -1,
            'salary': "N/A",
            'phone': "12345",
            'date': random.choice(self.INVALID_DATES),
            'id': "DUPLICATE",
            'rating': 10,
            'stock_quantity': -100,
            'name': "!!!@@@###",
            'quantity': -5,
            'price_per_unit': "free",
        }
        injected = errors.get(field_name, None)
        logger.debug(f"Injected error for field '{field_name}': {injected}")
        return injected

    def generate_email(self, first_name: Optional[str] = None, last_name: Optional[str] = None) -> str:
        if self.inject_errors and random.random() < self.error_prob / 2:
            malformed = random.choice(self.MALFORMED_EMAILS)
            logger.debug(f"Generated malformed email: {malformed}")
            return malformed
        if not first_name:
            first_name = random.choice(self.first_names)
        if not last_name:
            last_name = random.choice(self.last_names)
        domain = random.choice(self.domains)
        separator = random.choice([".", "_", ""])
        email = f"{first_name.lower()}{separator}{last_name.lower()}@{domain}"
        logger.debug(f"Generated email: {email}")
        return email

    def generate_phone(self) -> str:
        if self.inject_errors and random.random() < self.error_prob:
            logger.debug("Generated malformed phone number: 123")
            return "123"
        phone = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        logger.debug(f"Generated phone number: {phone}")
        return phone

    def generate_date(self, start_days_ago: int = 365, end_days_ago: int = 0) -> str:
        if self.inject_errors and random.random() < self.error_prob:
            invalid_date = random.choice(self.INVALID_DATES)
            logger.debug(f"Generated invalid date: {invalid_date}")
            return invalid_date
        start = datetime.now() - timedelta(days=start_days_ago)
        end = datetime.now() - timedelta(days=end_days_ago)
        rand = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
        date_str = rand.strftime("%Y-%m-%d")
        logger.debug(f"Generated date: {date_str}")
        return date_str

    def generate_tags(self, min_tags: int = 1, max_tags: int = 5) -> str:
        tags = random.sample(self.technologies, random.randint(min_tags, max_tags))
        joined_tags = ";".join(tags)
        logger.debug(f"Generated tags: {joined_tags}")
        return joined_tags

    def _generate_unique_ids(self, prefix: str, num: int) -> List[str]:
        ids = [f"{prefix}-{i:04d}" for i in range(1, num + 1)]
        if self.inject_errors and self.test_case_mode:
            # Add duplicates but limit length to num
            duplicates = ids[:self.duplicate_count]
            ids = (ids + duplicates)[:num]
            logger.debug(f"Injected duplicates for prefix {prefix}: {duplicates}")
        return ids

    def generate_csv_users(self, num_rows: int = 1000) -> str:
        filename = self.output_dir / "users.csv"
        ids = self._generate_unique_ids("USR", num_rows)
        corrupt_rows = 0

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.USER_FIELDS)
            writer.writeheader()
            for i in range(num_rows):
                idx = ids[i] if i < len(ids) else f"USR-{i+1:04d}"
                first = self.faker.first_name()
                last = self.faker.last_name()
                email = self.generate_email(first, last)
                phone = self.generate_phone()
                age = random.randint(22, 65)
                dept = random.choice(self.departments)
                status = random.choice(self.statuses)
                country = random.choice(self.countries)
                salary = random.randint(40000, 150000)
                hire_date = self.generate_date(1095, 30)
                skills = self.generate_tags(2, 6)
                projects = random.randint(1, 10)
                manager_email = self.generate_email() if random.random() > 0.2 else ""

                row = {
                    'id': self._maybe_inject_error(idx, 'id'),
                    'first_name': self._maybe_inject_error(first, 'name'),
                    'last_name': self._maybe_inject_error(last, 'name'),
                    'email': self._maybe_inject_error(email, 'email'),
                    'phone': self._maybe_inject_error(phone, 'phone'),
                    'age': self._maybe_inject_error(age, 'age'),
                    'department': dept,
                    'status': status,
                    'country': country,
                    'salary': self._maybe_inject_error(salary, 'salary'),
                    'hire_date': self._maybe_inject_error(hire_date, 'date'),
                    'skills': skills,
                    'projects': projects,
                    'manager_email': manager_email
                }
                writer.writerow(row)

            if self.inject_errors and self.test_case_mode:
                corrupt_rows += 1
                logger.debug("Adding explicit corrupt user row")
                writer.writerow({
                    'id': 'CORRUPT', 'first_name': '', 'last_name': '',
                    'email': '???', 'phone': 'abc', 'age': 'old',
                    'department': '', 'status': '', 'country': '',
                    'salary': 'none', 'hire_date': 'invalid-date',
                    'skills': '', 'projects': 'NaN', 'manager_email': ''
                })

        logger.info(f"✅ Generated {filename} with {num_rows} rows (+{corrupt_rows} corrupt rows)")
        return str(filename)

    def generate_csv_products(self, num_rows: int = 500) -> str:
        filename = self.output_dir / "products.csv"
        product_names = [
            "Laptop Pro", "Desktop Elite", "Monitor 4K", "Keyboard Wireless",
            "Mouse Gaming", "Headphones Premium", "Webcam HD", "Tablet Mini",
            "Phone Smart", "Watch Digital", "Speaker Bluetooth", "Camera DSLR",
            "Printer Laser", "Scanner Document", "Router WiFi"
        ]
        ids = self._generate_unique_ids("PROD", num_rows)
        corrupt_rows = 0

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.PRODUCT_FIELDS)
            writer.writeheader()
            for i in range(num_rows):
                idx = ids[i] if i < len(ids) else f"PROD-{i+1:04d}"
                name = f"{random.choice(product_names)} {random.choice(['X', 'Pro', 'Elite', 'Max', 'Mini'])}"
                cat = random.choice(self.categories)
                price = round(random.uniform(10.99, 2999.99), 2)
                stock = random.randint(0, 1000)
                supplier = self.generate_email()
                tags = self.generate_tags(1, 4)
                launch = self.generate_date(730, 0)
                rating = round(random.uniform(1.0, 5.0), 1)
                status = random.choice(self.statuses)

                row = {
                    'product_id': self._maybe_inject_error(idx, 'id'),
                    'name': self._maybe_inject_error(name, 'name'),
                    'category': cat,
                    'price': self._maybe_inject_error(price, 'salary'),
                    'stock_quantity': self._maybe_inject_error(stock, 'stock_quantity'),
                    'supplier_email': self._maybe_inject_error(supplier, 'email'),
                    'tags': tags,
                    'launch_date': self._maybe_inject_error(launch, 'date'),
                    'rating': self._maybe_inject_error(rating, 'rating'),
                    'status': status
                }
                writer.writerow(row)

            if self.inject_errors and self.test_case_mode:
                corrupt_rows += 1
                logger.debug("Adding explicit corrupt product row")
                writer.writerow({
                    'product_id': 'CORRUPT', 'name': '', 'category': '',
                    'price': 'free', 'stock_quantity': 'many', 'supplier_email': '???',
                    'tags': '', 'launch_date': 'invalid-date', 'rating': 'bad', 'status': ''
                })

        logger.info(f"✅ Generated {filename} with {num_rows} rows (+{corrupt_rows} corrupt rows)")
        return str(filename)

    def generate_json_orders(self, num_rows: int = 500) -> str:
        filename = self.output_dir / "orders.json"
        orders: List[Dict[str, Any]] = []
        corrupt_entries = 0

        user_ids = [f"USR-{i:04d}" for i in range(1, 1001)]
        product_ids = [f"PROD-{i:04d}" for i in range(1, 501)]

        for i in range(num_rows):
            order_id = f"ORD-{i+1:05d}"
            user = random.choice(user_ids)
            prod = random.choice(product_ids)
            qty = random.randint(1, 10)
            price = round(random.uniform(5.0, 1500.0), 2)
            order_date = self.generate_date(365, 0)
            status = random.choice(self.statuses)

            order = {
                'order_id': self._maybe_inject_error(order_id, 'id'),
                'user_id': self._maybe_inject_error(user, 'id'),
                'product_id': self._maybe_inject_error(prod, 'id'),
                'quantity': self._maybe_inject_error(qty, 'quantity'),
                'price_per_unit': self._maybe_inject_error(price, 'price_per_unit'),
                'order_date': self._maybe_inject_error(order_date, 'date'),
                'status': status,
            }
            orders.append(order)

        if self.inject_errors and self.test_case_mode:
            corrupt_entries += 1
            orders.append({
                'order_id': 'CORRUPT', 'user_id': '???', 'product_id': '!!!',
                'quantity': 'many', 'price_per_unit': 'cheap',
                'order_date': 'invalid-date', 'status': ''
            })

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2)

        logger.info(f"✅ Generated {filename} with {num_rows} entries (+{corrupt_entries} corrupt entries)")
        return str(filename)

    def generate_config(self) -> str:
        config = {
            'users': {
                'fields': self.USER_FIELDS,
                'file': 'users.csv',
                'delimiter': ',',
                'primary_key': 'id',
            },
            'products': {
                'fields': self.PRODUCT_FIELDS,
                'file': 'products.csv',
                'delimiter': ',',
                'primary_key': 'product_id',
            },
            'orders': {
                'fields': self.ORDER_FIELDS,
                'file': 'orders.json',
                'format': 'json',
                'primary_key': 'order_id',
            },
        }

        filename = self.config_dir / "config.yaml"
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, sort_keys=False)

        logger.info(f"✅ Generated config file {filename}")
        return str(filename)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate test data sets for users, products, and orders with optional error injection.",
        epilog=(
            "Example usage:\n"
            "  python generate_test_data.py --output-dir ./data --users 1000 --products 500 --orders 500\n"
            "  python generate_test_data.py --inject-errors --test-case-mode\n"
            "  python generate_test_data.py --file users products --verbose\n"
            "  python generate_test_data.py --config-dir ./configs\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--output-dir', type=str, default='test_data',
        help='Directory to output generated data files (default: test_data)'
    )
    parser.add_argument(
        '--config-dir', type=str, default=None,
        help='Directory to output config YAML file (default: <output-dir>/configs)'
    )
    parser.add_argument(
        '--faker-seed', type=int, default=42,
        help='Random seed for Faker and reproducibility (default: 42)'
    )
    parser.add_argument(
        '--inject-errors', action='store_true',
        help='Inject random data errors into the output files'
    )
    parser.add_argument(
        '--test-case-mode', action='store_true',
        help='Add explicit corrupt rows and duplicates for test cases (implies --inject-errors)'
    )
    parser.add_argument(
        '--error-prob', type=float, default=0.05,
        help='Probability of injecting an error in each field (default: 0.05)'
    )
    parser.add_argument(
        '--duplicate-count', type=int, default=5,
        help='Number of duplicates to add in test-case-mode (default: 5)'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Enable verbose debug logging'
    )
    parser.add_argument(
        '--file', nargs='+', choices=['users', 'products', 'orders', 'config'], default=['users', 'products', 'orders', 'config'],
        help='Which data files to generate (default: all)'
    )
    parser.add_argument(
        '--users', type=int, default=1000,
        help='Number of user rows to generate (default: 1000)'
    )
    parser.add_argument(
        '--products', type=int, default=500,
        help='Number of product rows to generate (default: 500)'
    )
    parser.add_argument(
        '--orders', type=int, default=500,
        help='Number of order entries to generate (default: 500)'
    )

    args = parser.parse_args()
    if args.test_case_mode:
        args.inject_errors = True  # test-case implies error injection

    return args


def main():
    args = parse_args()
    generator = TestDataGenerator(
        output_dir=args.output_dir,
        config_dir=args.config_dir,
        faker_seed=args.faker_seed,
        inject_errors=args.inject_errors,
        test_case_mode=args.test_case_mode,
        error_prob=args.error_prob,
        duplicate_count=args.duplicate_count,
        verbose=args.verbose
    )

    if 'users' in args.file:
        generator.generate_csv_users(num_rows=args.users)
    if 'products' in args.file:
        generator.generate_csv_products(num_rows=args.products)
    if 'orders' in args.file:
        generator.generate_json_orders(num_rows=args.orders)
    if 'config' in args.file:
        generator.generate_config()


if __name__ == '__main__':
    main()
