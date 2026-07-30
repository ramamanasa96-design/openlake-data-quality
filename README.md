# 🚀 OpenLake Data Quality

OpenLake Data Quality is a lightweight, open-source Python framework for validating, profiling, and reporting data quality issues before datasets enter analytics, machine learning, or ETL pipelines.

It supports **CSV, JSON, Parquet, and Excel** datasets and generates professional **HTML** and **JSON** reports.

---

# ✨ Features

- ✅ Read CSV files
- ✅ Read JSON files
- ✅ Read Parquet files
- ✅ Read Excel (.xlsx/.xls) files
- ✅ Detect missing values
- ✅ Detect duplicate rows
- ✅ Display column data types
- ✅ Schema validation
- ✅ Column profiling
- ✅ Numeric outlier detection
- ✅ Data quality scoring
- ✅ Interactive HTML report generation
- ✅ JSON report generation
- ✅ Command-line interface (CLI)

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/ramamanasa96-design/openlake-data-quality.git
```

Move into the project:

```bash
cd openlake-data-quality
```

Install dependencies:

```bash
pip install -r requirements.txt
```

or install the package in development mode:

```bash
pip install -e ".[dev]"
```

---

# ▶️ Basic Usage

Run OpenLake on a dataset:

```bash
python -m openlake.cli sample_data/employees.csv
```

or

```bash
openlake sample_data/employees.csv
```

---

# 📄 Generate Custom Reports

```bash
openlake sample_data/employees.csv \
    --output reports/employees_report.html \
    --json-output reports/employees_report.json
```

PowerShell (single line):

```powershell
openlake sample_data/employees.csv --output reports/employees_report.html --json-output reports/employees_report.json
```

---

# 📋 Validate Using a Schema

```bash
openlake sample_data/employees.csv --schema schema.json
```

Disable the default schema:

```bash
openlake sample_data/employees.csv --no-default-schema
```

---

# 📈 Configure Outlier Detection

Default Z-score threshold:

```
3.0
```

Example:

```bash
openlake sample_data/employees.csv --z-threshold 2.5
```

---

# 📊 Example Console Output

```
==================================================
OpenLake Data Quality Report
==================================================

Input File : sample_data/employees.csv

Rows       : 10
Columns    : 5
Duplicates : 1

Missing Values
------------------------------
email: 1

Data Types
------------------------------
id : int64
name : object
email : object
department : object
salary : int64

Outlier Summary
------------------------------
salary : 1

Schema Validation
------------------------------
Schema Status : PASSED

Data Quality Score
------------------------------
Overall Score   : 95.33 / 100
Completeness    : 98.00%
Uniqueness      : 90.00%
Schema Validity : 100.00%

Generated Reports
------------------------------
HTML Report : quality_report.html
JSON Report : quality_report.json
```

---

# 📑 HTML Report

The generated HTML report includes:

- Overall Quality Score
- Dataset Summary
- Missing Values
- Duplicate Summary
- Quality Score Chart
- Outlier Summary
- Data Types
- Column Profile
- Schema Validation Results

---

# 📂 Supported File Formats

- CSV
- JSON
- Parquet
- Excel (.xlsx/.xls)

---

# 📂 Project Structure

```
openlake-data-quality/
│
├── openlake/
│   ├── __init__.py
│   ├── cli.py
│   ├── profiler.py
│   ├── reader.py
│   ├── report.py
│   └── validator.py
│
├── sample_data/
│
├── tests/
│
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 🧪 Development

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

Run Ruff:

```bash
ruff check .
```

Build the package:

```bash
python -m build
```

---

# 📈 Data Quality Metrics

OpenLake calculates:

- Completeness Score
- Uniqueness Score
- Schema Validation Score
- Overall Quality Score

The overall score is calculated from the average of these metrics.

---

# 🛣️ Roadmap

## Completed

- ✅ CSV Reader
- ✅ JSON Reader
- ✅ Parquet Reader
- ✅ Excel Reader
- ✅ Missing Value Detection
- ✅ Duplicate Detection
- ✅ Data Type Detection
- ✅ Schema Validation
- ✅ Column Profiling
- ✅ Outlier Detection
- ✅ HTML Reports
- ✅ JSON Reports
- ✅ CLI Support

## Planned

- ⏳ Unit Tests
- ⏳ GitHub Actions
- ⏳ PyPI Publishing
- ⏳ AWS S3 Integration
- ⏳ Databricks Integration
- ⏳ Database Connectors
- ⏳ Data Drift Detection
- ⏳ Streamlit Dashboard
- ⏳ PDF Reports

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Rama Rayudu Gangumalla**

GitHub:
https://github.com/ramamanasa96-design

---

⭐ If you found this project useful, consider giving it a star on GitHub.