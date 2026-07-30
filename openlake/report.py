import json
from pathlib import Path
from typing import Any


def generate_html_report(
    report_data: dict[str, Any],
    output_path: str = "quality_report.html",
) -> str:
    """
    Generate an HTML data quality report.

    Args:
        report_data: Dictionary containing validation results and scores.
        output_path: Path where the HTML report should be saved.

    Returns:
        The saved report path.
    """
    missing_values = report_data["missing_values"]
    data_types = report_data["data_types"]
    schema_result = report_data["schema_result"]
    quality_scores = report_data["quality_scores"]

    missing_rows = "".join(
        f"<tr><td>{column}</td><td>{count}</td></tr>"
        for column, count in missing_values.items()
    )

    if not missing_rows:
        missing_rows = (
            "<tr><td colspan='2'>No missing values found</td></tr>"
        )

    data_type_rows = "".join(
        f"<tr><td>{column}</td><td>{data_type}</td></tr>"
        for column, data_type in data_types.items()
    )

    schema_status = (
        "PASSED" if schema_result["is_valid"] else "FAILED"
    )

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>OpenLake Data Quality Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 30px;
            color: #222;
        }}

        .container {{
            max-width: 1000px;
            margin: auto;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        .subtitle {{
            color: #666;
            margin-bottom: 25px;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }}

        .card h3 {{
            margin-top: 0;
            color: #555;
        }}

        .score {{
            font-size: 28px;
            font-weight: bold;
        }}

        .section {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th,
        td {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background: #f0f2f5;
        }}

        .passed {{
            color: #16803d;
            font-weight: bold;
        }}

        .failed {{
            color: #c62828;
            font-weight: bold;
        }}
    </style>
</head>

<body>
    <div class="container">
        <h1>OpenLake Data Quality Report</h1>
        <div class="subtitle">
            Automated validation, profiling, and schema checks
        </div>

        <div class="cards">
            <div class="card">
                <h3>Overall Score</h3>
                <div class="score">
                    {quality_scores["overall_score"]} / 100
                </div>
            </div>

            <div class="card">
                <h3>Rows</h3>
                <div class="score">{report_data["rows"]}</div>
            </div>

            <div class="card">
                <h3>Columns</h3>
                <div class="score">{report_data["columns"]}</div>
            </div>

            <div class="card">
                <h3>Duplicates</h3>
                <div class="score">{report_data["duplicate_rows"]}</div>
            </div>
        </div>

        <div class="section">
            <h2>Quality Scores</h2>

            <table>
                <tr>
                    <th>Metric</th>
                    <th>Score</th>
                </tr>
                <tr>
                    <td>Completeness</td>
                    <td>{quality_scores["completeness_score"]}%</td>
                </tr>
                <tr>
                    <td>Uniqueness</td>
                    <td>{quality_scores["uniqueness_score"]}%</td>
                </tr>
                <tr>
                    <td>Schema Validity</td>
                    <td>{quality_scores["schema_score"]}%</td>
                </tr>
            </table>
        </div>

        <div class="section">
            <h2>Missing Values</h2>

            <table>
                <tr>
                    <th>Column</th>
                    <th>Missing Count</th>
                </tr>
                {missing_rows}
            </table>
        </div>

        <div class="section">
            <h2>Data Types</h2>

            <table>
                <tr>
                    <th>Column</th>
                    <th>Data Type</th>
                </tr>
                {data_type_rows}
            </table>
        </div>

        <div class="section">
            <h2>Schema Validation</h2>

            <p class="{
                "passed" if schema_result["is_valid"] else "failed"
            }">
                Schema Status: {schema_status}
            </p>
        </div>
    </div>
</body>
</html>
"""

    report_path = Path(output_path)
    report_path.write_text(html, encoding="utf-8")

    return str(report_path)


def generate_json_report(
    report_data: dict[str, Any],
    output_path: str = "quality_report.json",
) -> str:
    """
    Generate a JSON data quality report.

    Args:
        report_data: Dictionary containing validation results and scores.
        output_path: Path where the JSON report should be saved.

    Returns:
        The saved report path.
    """
    report_path = Path(output_path)

    report_path.write_text(
        json.dumps(report_data, indent=2),
        encoding="utf-8",
    )

    return str(report_path)