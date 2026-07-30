import argparse

from openlake.profiler import calculate_quality_score
from openlake.reader import read_dataset
from openlake.report import generate_html_report
from openlake.validator import (
    count_duplicate_rows,
    find_missing_values,
    get_data_types,
    validate_schema,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openlake",
        description=(
            "Validate CSV, JSON, and Parquet datasets and generate "
            "a data quality report."
        ),
    )

    parser.add_argument(
        "file_path",
        nargs="?",
        default="sample_data/employees.csv",
        help="Path to a CSV, JSON, or Parquet dataset.",
    )

    parser.add_argument(
        "--output",
        default="quality_report.html",
        help="Path for the generated HTML report.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    df = read_dataset(args.file_path)

    missing_values = find_missing_values(df)
    duplicate_rows = count_duplicate_rows(df)
    data_types = get_data_types(df)

    expected_schema = {
        "id": "int64",
        "name": "str",
        "email": "str",
        "department": "str",
        "salary": "int64",
    }

    schema_result = validate_schema(df, expected_schema)

    quality_scores = calculate_quality_score(
        df=df,
        duplicate_rows=duplicate_rows,
        schema_is_valid=schema_result["is_valid"],
    )

    print("=" * 50)
    print("OpenLake Data Quality Report")
    print("=" * 50)
    print(f"Input File : {args.file_path}")
    print(f"Rows       : {df.shape[0]}")
    print(f"Columns    : {df.shape[1]}")
    print(f"Duplicates : {duplicate_rows}")

    print("\nMissing Values")
    print("-" * 30)

    if missing_values:
        for column, count in missing_values.items():
            print(f"{column}: {count}")
    else:
        print("No missing values found")

    print("\nData Types")
    print("-" * 30)

    for column, data_type in data_types.items():
        print(f"{column}: {data_type}")

    print("\nSchema Validation")
    print("-" * 30)

    if schema_result["is_valid"]:
        print("Schema Status: PASSED")
    else:
        print("Schema Status: FAILED")

        if schema_result["missing_columns"]:
            print("\nMissing Columns")
            for column in schema_result["missing_columns"]:
                print(f"- {column}")

        if schema_result["unexpected_columns"]:
            print("\nUnexpected Columns")
            for column in schema_result["unexpected_columns"]:
                print(f"- {column}")

        if schema_result["type_mismatches"]:
            print("\nType Mismatches")
            for column, mismatch in schema_result["type_mismatches"].items():
                print(
                    f"- {column}: expected {mismatch['expected']}, "
                    f"found {mismatch['actual']}"
                )

    print("\nData Quality Score")
    print("-" * 30)
    print(f"Overall Score   : {quality_scores['overall_score']} / 100")
    print(f"Completeness    : {quality_scores['completeness_score']}%")
    print(f"Uniqueness      : {quality_scores['uniqueness_score']}%")
    print(f"Schema Validity : {quality_scores['schema_score']}%")

    report_data = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicate_rows": duplicate_rows,
        "missing_values": missing_values,
        "data_types": data_types,
        "schema_result": schema_result,
        "quality_scores": quality_scores,
    }

    report_path = generate_html_report(
        report_data=report_data,
        output_path=args.output,
    )

    print("\nHTML Report")
    print("-" * 30)
    print(f"Generated: {report_path}")


if __name__ == "__main__":
    main()