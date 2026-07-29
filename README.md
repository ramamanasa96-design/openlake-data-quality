# 🚀 OpenLake Data Quality

A lightweight, open-source Python framework for validating, profiling, and reporting data quality issues in CSV, JSON, and Parquet datasets before they enter analytics and ETL pipelines.

---

## ✨ Features

- ✅ Read CSV, JSON and Parquet files
- ✅ Detect missing values
- ✅ Detect duplicate rows
- ✅ Display column data types
- 🚧 Schema validation (Coming Soon)
- 🚧 Quality score (Coming Soon)
- 🚧 HTML reports (Coming Soon)
- 🚧 AWS S3 support (Coming Soon)
- 🚧 Databricks integration (Coming Soon)

---

## 📦 Installation

```bash
git clone https://github.com/ramamanasa96-design/openlake-data-quality.git

cd openlake-data-quality

pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python -m openlake.cli
```

---

## Example Output

```
OpenLake Data Quality Report

Rows       : 6
Columns    : 5
Duplicates : 1

Missing Values

email: 1

department: 1

Data Types

id : int64
name : object
email : object
department : object
salary : int64
```

---

## 📂 Project Structure

```
openlake-data-quality/
│
├── docs/
├── examples/
├── openlake/
│   ├── reader.py
│   ├── validator.py
│   ├── profiler.py
│   ├── report.py
│   └── cli.py
│
├── sample_data/
├── tests/
├── requirements.txt
└── README.md
```

---

## 🛣️ Roadmap

- [x] Dataset Reader
- [x] Missing Value Detection
- [x] Duplicate Detection
- [x] Data Type Detection
- [ ] Schema Validation
- [ ] Data Profiling
- [ ] HTML Reports
- [ ] JSON Reports
- [ ] CLI Commands
- [ ] Unit Tests
- [ ] GitHub Actions
- [ ] AWS S3 Support
- [ ] Databricks Integration
- [ ] PyPI Package

---

## 🤝 Contributing

Contributions are welcome.

Please open an Issue first before submitting a Pull Request.

---

## 📄 License

MIT License