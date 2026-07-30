import html
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
        report_data: Dictionary containing validation,
            profiling, outlier, and score information.
        output_path: Path where the HTML report should be saved.

    Returns:
        The saved HTML report path.
    """
    quality_scores = report_data["quality_scores"]
    schema_result = report_data["schema_result"]

    missing_rows = "".join(
        (
            "<tr>"
            f"<td>{html.escape(str(column))}</td>"
            f"<td>{count}</td>"
            "</tr>"
        )
        for column, count in report_data["missing_values"].items()
    )

    if not missing_rows:
        missing_rows = (
            "<tr>"
            "<td colspan='2'>No missing values found</td>"
            "</tr>"
        )

    data_type_rows = "".join(
        (
            "<tr>"
            f"<td>{html.escape(str(column))}</td>"
            f"<td>{html.escape(str(data_type))}</td>"
            "</tr>"
        )
        for column, data_type in report_data["data_types"].items()
    )

    outlier_rows = "".join(
        (
            "<tr>"
            f"<td>{html.escape(str(column))}</td>"
            f"<td>{count}</td>"
            "</tr>"
        )
        for column, count in report_data["outliers"].items()
    )

    if not outlier_rows:
        outlier_rows = (
            "<tr>"
            "<td colspan='2'>No numeric columns found</td>"
            "</tr>"
        )

    profile_rows = "".join(
        (
            "<tr>"
            f"<td>{html.escape(str(column))}</td>"
            f"<td>{html.escape(str(values.get('data_type', '')))}</td>"
            f"<td>{values.get('non_null_count', '')}</td>"
            f"<td>{values.get('missing_count', '')}</td>"
            f"<td>{values.get('unique_count', '')}</td>"
            f"<td>{format_profile_value(values.get('minimum'))}</td>"
            f"<td>{format_profile_value(values.get('maximum'))}</td>"
            f"<td>{format_profile_value(values.get('mean'))}</td>"
            f"<td>{format_profile_value(values.get('median'))}</td>"
            "</tr>"
        )
        for column, values in report_data["column_profile"].items()
    )

    schema_status = (
        "PASSED"
        if schema_result["is_valid"]
        else "FAILED"
    )

    schema_class = (
        "passed"
        if schema_result["is_valid"]
        else "failed"
    )

    schema_details = build_schema_details(
        schema_result
    )

    chart_data = json.dumps(
        [
            quality_scores["completeness_score"],
            quality_scores["uniqueness_score"],
            quality_scores["schema_score"],
        ]
    )

    html_document = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>OpenLake Data Quality Report</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            color: #222;
            margin: 0;
            padding: 30px;
        }}

        .container {{
            max-width: 1150px;
            margin: auto;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        h2 {{
            margin-top: 0;
        }}

        .subtitle {{
            color: #666;
            margin-bottom: 20px;
        }}

        .section,
        .card,
        .input-file {{
            background: white;
            border-radius: 10px;
            box-shadow:
                0 2px 8px rgba(0, 0, 0, 0.08);
        }}

        .input-file {{
            padding: 15px 20px;
            margin-bottom: 20px;
            word-break: break-word;
        }}

        .cards {{
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .card {{
            padding: 20px;
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
            padding: 20px;
            margin-bottom: 20px;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th,
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
            text-align: left;
            white-space: nowrap;
        }}

        th {{
            background: #f0f2f5;
        }}

        tbody tr:hover {{
            background: #fafafa;
        }}

        .passed {{
            color: #16803d;
            font-weight: bold;
        }}

        .failed {{
            color: #c62828;
            font-weight: bold;
        }}

        .chart-wrapper {{
            height: 350px;
        }}

        .footer {{
            text-align: center;
            color: #777;
            font-size: 13px;
            padding: 15px;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 15px;
            }}

            .score {{
                font-size: 23px;
            }}

            .section {{
                padding: 15px;
            }}
        }}
    </style>
</head>

<body>
    <div class="container">
        <h1>OpenLake Data Quality Report</h1>

        <div class="subtitle">
            Automated validation, profiling,
            scoring, and outlier checks
        </div>

        <div class="input-file">
            <strong>Input File:</strong>
            {
                html.escape(
                    str(
                        report_data.get(
                            "input_file",
                            "Not provided",
                        )
                    )
                )
            }
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

                <div class="score">
                    {report_data["rows"]}
                </div>
            </div>

            <div class="card">
                <h3>Columns</h3>

                <div class="score">
                    {report_data["columns"]}
                </div>
            </div>

            <div class="card">
                <h3>Duplicates</h3>

                <div class="score">
                    {report_data["duplicate_rows"]}
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Quality Score Overview</h2>

            <div class="chart-wrapper">
                <canvas id="qualityChart"></canvas>
            </div>
        </div>

        <div class="section">
            <h2>Quality Scores</h2>

            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Score</th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td>Completeness</td>

                        <td>
                            {
                                quality_scores[
                                    "completeness_score"
                                ]
                            }%
                        </td>
                    </tr>

                    <tr>
                        <td>Uniqueness</td>

                        <td>
                            {
                                quality_scores[
                                    "uniqueness_score"
                                ]
                            }%
                        </td>
                    </tr>

                    <tr>
                        <td>Schema Validity</td>

                        <td>
                            {
                                quality_scores[
                                    "schema_score"
                                ]
                            }%
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Missing Values</h2>

            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Missing Count</th>
                    </tr>
                </thead>

                <tbody>
                    {missing_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Outlier Summary</h2>

            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Outlier Count</th>
                    </tr>
                </thead>

                <tbody>
                    {outlier_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Data Types</h2>

            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Data Type</th>
                    </tr>
                </thead>

                <tbody>
                    {data_type_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Column Profile</h2>

            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Type</th>
                        <th>Non-null</th>
                        <th>Missing</th>
                        <th>Unique</th>
                        <th>Minimum</th>
                        <th>Maximum</th>
                        <th>Mean</th>
                        <th>Median</th>
                    </tr>
                </thead>

                <tbody>
                    {profile_rows}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Schema Validation</h2>

            <p class="{schema_class}">
                Schema Status: {schema_status}
            </p>

            {schema_details}
        </div>

        <div class="footer">
            Generated by OpenLake Data Quality
        </div>
    </div>

    <script>
        const chartElement = document.getElementById(
            "qualityChart"
        );

        new Chart(chartElement, {{
            type: "bar",

            data: {{
                labels: [
                    "Completeness",
                    "Uniqueness",
                    "Schema Validity"
                ],

                datasets: [
                    {{
                        label: "Quality Score",

                        data: {chart_data},

                        backgroundColor: [
                            "rgba(54, 162, 235, 0.7)",
                            "rgba(255, 159, 64, 0.7)",
                            "rgba(75, 192, 192, 0.7)"
                        ],

                        borderWidth: 1
                    }}
                ]
            }},

            options: {{
                responsive: true,
                maintainAspectRatio: false,

                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    report_path = Path(output_path)

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        html_document,
        encoding="utf-8",
    )

    return str(report_path)


def generate_json_report(
    report_data: dict[str, Any],
    output_path: str = "quality_report.json",
) -> str:
    """
    Generate a JSON data quality report.

    Args:
        report_data: Dictionary containing report results.
        output_path: Path where the JSON report should be saved.

    Returns:
        The saved JSON report path.
    """
    report_path = Path(output_path)

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        json.dumps(
            report_data,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    return str(report_path)


def build_schema_details(
    schema_result: dict[str, Any],
) -> str:
    """
    Build HTML describing schema validation problems.
    """
    if schema_result["is_valid"]:
        return "<p>No schema issues were detected.</p>"

    sections: list[str] = []

    missing_columns = schema_result.get(
        "missing_columns",
        [],
    )

    if missing_columns:
        items = "".join(
            f"<li>{html.escape(str(column))}</li>"
            for column in missing_columns
        )

        sections.append(
            f"""
            <h3>Missing Columns</h3>
            <ul>{items}</ul>
            """
        )

    unexpected_columns = schema_result.get(
        "unexpected_columns",
        [],
    )

    if unexpected_columns:
        items = "".join(
            f"<li>{html.escape(str(column))}</li>"
            for column in unexpected_columns
        )

        sections.append(
            f"""
            <h3>Unexpected Columns</h3>
            <ul>{items}</ul>
            """
        )

    type_mismatches = schema_result.get(
        "type_mismatches",
        {},
    )

    if type_mismatches:
        items = "".join(
            (
                "<li>"
                f"{html.escape(str(column))}: "
                f"expected "
                f"{html.escape(str(details['expected']))}, "
                f"found "
                f"{html.escape(str(details['actual']))}"
                "</li>"
            )
            for column, details
            in type_mismatches.items()
        )

        sections.append(
            f"""
            <h3>Type Mismatches</h3>
            <ul>{items}</ul>
            """
        )

    return "".join(sections)


def format_profile_value(
    value: Any,
) -> str:
    """
    Format a column-profile value for HTML output.
    """
    if value is None:
        return "-"

    return html.escape(str(value))