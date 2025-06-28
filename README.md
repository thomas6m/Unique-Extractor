# 📊 Unique Value Extractor

A Python CLI tool to extract **unique values** from datasets in **CSV, JSON, YAML, or Parquet** formats. Supports **interactive filtering**, **custom output formats**, and flexible **row/column layouts**.

---

## ✨ Features

- ✅ Supports CSV, JSON, YAML, and Parquet input files
- 🔍 Interactive filtering with field-level value previews
- 🧪 Extract unique values from any column (including exploded `contact_ids`)
- 💾 Output to **CSV**, **JSON**, **YAML**, or **Parquet**
- 🔃 Output layout: single-row or multi-row
- 🧩 Custom column names and separators
- 🧠 Reports memory usage and runtime
- 📓 Logs operations to `extractor.log`

---

## 📦 Requirements

Install the required packages:

```bash
pip install polars psutil PyYAML
