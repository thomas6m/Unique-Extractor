README.md

# 🔍 Unique Extractor (Polars-powered)

A blazing-fast Python tool to **extract unique values** from large CSV files using [Polars](https://pola.rs), with full support for **interactive prompts** and **command-line automation**.

---

## 📚 Table of Contents

- [🚀 Features](#-features)
- [⚙️ Requirements](#️-requirements)
- [🧑‍💻 Usage Options](#-usage-options)
  - [▶️ CLI Mode](#️-cli-mode)
  - [🧭 Interactive Mode](#-interactive-mode)
- [🔧 Command-Line Arguments](#-command-line-arguments)
- [📤 Output Modes](#-output-modes)
- [🔍 Filter Format](#-filter-format)
- [✨ Special Handling: `contact_ids`](#-special-handling-contact_ids)
- [🪵 Logging & Monitoring](#-logging--monitoring)
- [🧯 Troubleshooting](#-troubleshooting)
- [🧪 Example Test Run](#-example-test-run)
- [🧰 Virtual Environment Setup](#-virtual-environment-setup)
- [📦 Optional Enhancements](#-optional-enhancements)
- [📄 License](#-license)

---

## 🚀 Features

✅ CLI and interactive hybrid interface  
✅ Filter by **any combination of fields**  
✅ Extract from any field (e.g., `contact_ids`, `namespace`)  
✅ Single-row or multi-row output  
✅ Custom column name, separator, and CSV delimiter  
✅ Cleans and trims data, ignores blanks  
✅ Logging to `extractor.log`  
✅ Runtime and memory usage tracking via `psutil`  
✅ Safe file overwrite prompts  
✅ Ideal for both scripting and exploration

---

## ⚙️ Requirements

- Python **3.8+**
- [`polars`](https://pypi.org/project/polars/)
- [`psutil`](https://pypi.org/project/psutil/)

### 🔧 Install Dependencies


pip install -r requirements.txt


requirements.txt:

polars
psutil


🧑‍💻 Usage Options

▶️ CLI Mode
Provide all required arguments for full automation:


python extract_unique_values.py \
  --input data.csv \
  --output result.csv \
  --unique-field contact_ids \
  --row-format multi \
  --separator ";" \
  --column-name unique_contacts \
  clustername=apacgcb0001d region=apac
  
  
🧭 Interactive Mode
If you omit any of the following arguments, the script will prompt you:

Filters
Unique field
Separator
Column name
Row format
Output file path

python extract_unique_values.py --input data.csv

Sample interaction:


📌 Available fields: region, clustername, contact_ids
Field name (leave empty to stop): region
Enter comma-separated values for region: apac,emea

🎯 Available fields: region, clustername, contact_ids
Select the field to extract unique values from: contact_ids

Enter separator for unique values (default ';'):

Enter custom column name (default 'unique_contact_ids'):

Row format? (single/multi) [default=single]:

🔎 Unique values found:
 - abc123
 - def456
 - xyz789

💾 Save results to CSV? (y/n): y
Output file name: contacts_apac.csv

✅ Output saved to: contacts_apac.csv
⏱️ Time taken: 0.45s | 🧠 Memory used: 8.74 MB


🔧 Command-Line Arguments
Flag				Description
--input	(Required) 	Path to the input CSV file
--output			Output CSV path (optional)
--unique-field		Column to extract unique values from
--row-format		single or multi (default = single)
--separator			Separator for single-row values (default = ;)
--column-name		Custom name for output column
--delimiter			Input CSV delimiter (default = ,)
--verbose			Enable debug-level logging
filters	Field=value1,value2,... (space-separated)

📤 Output Modes
🔹 Single-row Output (--row-format single)


filters,unique_contact_ids
region=apac;clustername=node01,abc123;def456
🔹 Multi-row Output (--row-format multi)

unique_contact_ids
abc123
def456


🔍 Filter Format
You can pass filters via CLI or interactively.

CLI Format

region=apac clustername=node01
Interactive Format

Field name: region
Enter comma-separated values for region: apac,emea


✨ Special Handling: contact_ids
If --unique-field is set to contact_ids, the script:

Splits comma-separated strings
Trims each ID
Removes duplicates and nulls

🪵 Logging & Monitoring
All activity is logged to extractor.log
Tracks execution time and memory usage:


⏱️ Time taken: 1.23s | 🧠 Memory used: 10.45 MB

🧯 Troubleshooting
Problem	Solution
File not found	Check the --input file path
Invalid column	Ensure field names match CSV header
No values returned	Try different filters or check data format
Too many prompts	Use full CLI mode with all arguments

🧪 Example Test Run
Sample CSV: sample.csv

region,clustername,contact_ids
apac,apacgcb0001d,"abc123, def456"
emea,emeagcb0002d,"xyz789"
apac,apacgcb0001d,"def456"
Example Command:

python extract_unique_values.py --input sample.csv --unique-field contact_ids region=apac
Output:

unique_contact_ids
abc123
def456

🧰 Virtual Environment Setup


python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt

📦 Optional Enhancements
Want to build further?

✅ Package with pyproject.toml
✅ Add unit tests via pytest
✅ Build a Docker container
✅ Add TUI with textual

📄 License
MIT License — free to use, modify, and distribute.
