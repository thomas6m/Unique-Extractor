📊 Unique Value Extractor


A Python CLI tool to extract unique values from datasets in CSV, JSON, YAML, or Parquet formats. Supports filtering, custom output formats, and flexible row/column layouts.

✨ Features

✅ Supports CSV, JSON, YAML, and Parquet input files
🔍 Interactive field filtering with value preview
🧪 Extract unique values from any column (including exploded contact_ids)
💾 Output to CSV, JSON, YAML, or Parquet
🔃 Choose between single-row or multi-row format
⚙️ Custom column names and value separators
🧠 Memory usage and performance reporting
📓 Logs activity to extractor.log


📦 Requirements

Install Python dependencies:


pip install polars psutil PyYAML

Optional: use a requirements.txt file:


polars>=0.20.0
psutil>=5.9.0
PyYAML>=6.0

pip install -r requirements.txt

🚀 Usage
🖥️ Interactive Mode

python extract_unique_values.py

You’ll be prompted to:
Provide input file path
Choose filters for any field
Select a column to extract unique values
Choose row format (single/multi)
Set output file name and format (csv, json, yaml, or parquet)

⚙️ Command-Line Mode

python extract_unique_values.py \
  --input /data/input.csv \
  --output results.json \
  --unique-field contact_ids \
  --row-format multi \
  --column-name contacts \
  region=apac sector=gcb
  
  
Common CLI options:
Option				Description
--input				Path to input file (CSV, JSON, YAML, Parquet)
--output			Output file name with extension (e.g., output.csv)
--unique-field		Field to extract unique values from
--separator			Separator for single-row output (default: ;)
--column-name		Custom column name in the output file
--row-format		Single or multi (default: single)
--delimiter			CSV delimiter (default: ,)
--verbose			Enable verbose logging

filters	Optional filters in the form: field=value1,value2,...

📤 Output Formats

When saving results, the tool supports:
.csv 		– Standard CSV
.json 		– JSON object list
.yaml 		– YAML structure
.parquet 	– Apache Parquet (efficient columnar format)

The format is determined by either:

CLI --output file extension, or

Interactive prompt

🧪 Output Examples
🔹 Multi-row CSV:

unique_contact_ids
abc@example.com
xyz@example.com

🔸 Single-row JSON:

{
  "filters": "region=apac, sector=gcb",
  "unique_contact_ids": "abc@example.com;xyz@example.com"
}

📝 Logging
Logs are saved in extractor.log with timestamps and error messages.

✅ Example Session


📂 Enter path to input file (CSV, JSON, YAML, or Parquet): /data/sample.parquet

📌 Available fields: region, sector, environment, contact_ids
Field name (leave empty to stop): region
🔹 Available values for 'region': apac, emea
Enter comma-separated values for region: apac
...

🎯 Available fields: ...
Select the field to extract unique values from: contact_ids
Enter separator for unique values (default ';'): ;
Enter custom column name (default 'unique_contact_ids'):
Row format? (single/multi) [default=single]: single
💾 Save results? (y/n): y
Output file name (without extension): filtered_contacts
Select output format (csv, json, yaml, parquet) [default=csv]: json
✅ Output saved to: filtered_contacts.json

🧠 System Resource Summary
After execution, the tool reports time taken and memory used:

⏱️ Time taken: 1.47s | 🧠 Memory used: 33.82 MB

🔐 License
This script is provided "as-is" without warranty. You may customize and adapt it for internal or commercial use.

