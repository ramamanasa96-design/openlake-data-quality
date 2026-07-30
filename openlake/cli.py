import argparse
import json
import sys
from pathlib import Path
from typing import Any

from openlake.profiler import (
    calculate_quality_score,
    profile_columns,
)
from openlake.reader import read_dataset
from openlake.report import (
    generate_html_report,
    generate_json_report,
)
from openlake.validator import (
    count_duplicate_rows,
    detect_outliers,
    find_missing_values,
    get_data_types,
    validate_schema,
)


DEFAULT_SCHEMA = {
    "id": "int64",
    "name": "str",
    "email": "str",
    "department": "str",
    "salary": "int64",
}


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="openlake",
        description=(
            "Validate CSV, JSON, Parquet, and Excel datasets "
            "and generate HTML and JSON data quality reports."
        ),
    )

    parser.add_argument(
        "file_path",
        nargs="?",
        default="sample_data/employees.csv",
        help=(
            "Path to a CSV, JSON, Parquet, or Excel dataset."
        ),
    )

    parser.add_argument(
        "--output",
        default="quality_report.html",
        help="Path for the generated HTML report.",
    )

    parser.add_argument(
        "--json-output",
        default="quality_report.json",
        help="Path for the generated JSON report.",
    )

    parser.add_argument(
        "--schema",
        help=(
            "Optional path to a JSON schema file that maps "
            "column names to expected data types."
        ),
    )

    parser.add_argument(
        "--no-default-schema",
        action="store_true",
        help=(
            "Disable the built-in employee sample schema."
        ),
    )

    parser.add_argument(
        "--z-threshold",
        type=float,
        default=3.0,
        help=(
            "Z-score threshold used for numeric outlier "
            "detection. Default: 3.0"
        ),
    )

    return parser


def load_schema(
    args: argparse.Namespace,
) -> dict[str, str] | None:
    """
    Load a custom schema or return the default schema.

    Args:
        args: Parsed command-line arguments.

    Returns:
        A schema dictionary or None.
    """
    if args.schema:
        schema_path = Path(args.schema)

        if not schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {args.schema}"
            )

        schema_data = json.loads(
            schema_path.read_text(
                encoding="utf-8",
            )
        )

        if not isinstance(schema_data, dict):
            raise ValueError(
                "Schema file must contain a JSON object."
            )

        return {
            str(column): str(data_type)
            for column, data_type
            in schema_data.items()
        }

    if args.no_default_schema:
        return None

    return DEFAULT_SCHEMA


def build_report_data(
    file_path: str,
    expected_schema: dict[str, str] | None,
    z_threshold: float,
) -> dict[str, Any]:
    """
    Read and analyze a dataset.

    Args:
        file_path: Path to the dataset.
        expected_schema: Optional expected schema.
        z_threshold: Z-score threshold for outlier detection.

    Returns:
        Complete report data.
    """
    df = read_dataset(file_path)

    missing_values = find_missing_values(df)
    duplicate_rows = count_duplicate_rows(df)
    data_types = get_data_types(df)

    schema_result = validate_schema(
        df=df,
        expected_schema=expected_schema,
    )

    outliers = detect_outliers(
        df=df,
        z_threshold=z_threshold,
    )

    column_profile = profile_columns(df)

    quality_scores = calculate_quality_score(
        df=df,
        duplicate_rows=duplicate_rows,
        schema_is_valid=schema_result["is_valid"],
    )

    return {
        "input_file": file_path,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "duplicate_rows": duplicate_rows,
        "missing_values": missing_values,
        "data_types": data_types,
        "schema_result": schema_result,
        "quality_scores": quality_scores,
        "outliers": outliers,
        "column_profile": column_profile,
    }


def print_missing_values(
    missing_values: dict[str, int],
) -> None:
    """
    Print missing-value results.
    """
    print("\nMissing Values")
    print("-" * 30)

    if not missing_values:
        print("No missing values found")
        return

    for column, count in missing_values.items():
        print(f"{column}: {count}")


def print_data_types(
    data_types: dict[str, str],
) -> None:
    """
    Print detected data types.
    """
    print("\nData Types")
    print("-" * 30)

    for column, data_type in data_types.items():
        print(f"{column}: {data_type}")


def print_outliers(
    outliers: dict[str, int],
) -> None:
    """
    Print numeric outlier counts.
    """
    print("\nOutlier Summary")
    print("-" * 30)

    if not outliers:
        print("No numeric columns found")
        return

    for column, count in outliers.items():
        print(f"{column}: {count}")


def print_schema_result(
    schema_result: dict[str, Any],
) -> None:
    """
    Print schema validation results.
    """
    print("\nSchema Validation")
    print("-" * 30)

    if schema_result["is_valid"]:
        print("Schema Status: PASSED")
        return

    print("Schema Status: FAILED")

    missing_columns = schema_result.get(
        "missing_columns",
        [],
    )

    if missing_columns:
        print("\nMissing Columns")

        for column in missing_columns:
            print(f"- {column}")

    unexpected_columns = schema_result.get(
        "unexpected_columns",
        [],
    )

    if unexpected_columns:
        print("\nUnexpected Columns")

        for column in unexpected_columns:
            print(f"- {column}")

    type_mismatches = schema_result.get(
        "type_mismatches",
        {},
    )

    if type_mismatches:
        print("\nType Mismatches")

        for column, mismatch in type_mismatches.items():
            print(
                f"- {column}: "
                f"expected {mismatch['expected']}, "
                f"found {mismatch['actual']}"
            )


def print_quality_scores(
    quality_scores: dict[str, float],
) -> None:
    """
    Print calculated quality scores.
    """
    print("\nData Quality Score")
    print("-" * 30)

    print(
        "Overall Score   : "
        f"{quality_scores['overall_score']} / 100"
    )

    print(
        "Completeness    : "
        f"{quality_scores['completeness_score']}%"
    )

    print(
        "Uniqueness      : "
        f"{quality_scores['uniqueness_score']}%"
    )

    print(
        "Schema Validity : "
        f"{quality_scores['schema_score']}%"
    )


def print_summary(
    report_data: dict[str, Any],
) -> None:
    """
    Print complete command-line report output.
    """
    print("=" * 50)
    print("OpenLake Data Quality Report")
    print("=" * 50)

    print(
        f"Input File : {report_data['input_file']}"
    )

    print(
        f"Rows       : {report_data['rows']}"
    )

    print(
        f"Columns    : {report_data['columns']}"
    )

    print(
        "Duplicates : "
        f"{report_data['duplicate_rows']}"
    )

    print_missing_values(
        report_data["missing_values"]
    )

    print_data_types(
        report_data["data_types"]
    )

    print_outliers(
        report_data["outliers"]
    )

    print_schema_result(
        report_data["schema_result"]
    )

    print_quality_scores(
        report_data["quality_scores"]
    )


def main() -> int:
    """
    Run the OpenLake command-line application.
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        expected_schema = load_schema(args)

        report_data = build_report_data(
            file_path=args.file_path,
            expected_schema=expected_schema,
            z_threshold=args.z_threshold,
        )

        html_report_path = generate_html_report(
            report_data=report_data,
            output_path=args.output,
        )

        json_report_path = generate_json_report(
            report_data=report_data,
            output_path=args.json_output,
        )

        print_summary(report_data)

        print("\nGenerated Reports")
        print("-" * 30)

        print(
            f"HTML Report: {html_report_path}"
        )

        print(
            f"JSON Report: {json_report_path}"
        )

        return 0

    except (
        FileNotFoundError,
        ValueError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())