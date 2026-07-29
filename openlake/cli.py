from openlake.reader import read_dataset
from openlake.validator import (
    count_duplicate_rows,
    find_missing_values,
    get_data_types,
    validate_schema,
)


def main() -> None:
    df = read_dataset("sample_data/employees.csv")

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

    print("=" * 50)
    print("OpenLake Data Quality Report")
    print("=" * 50)

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

        missing_columns = schema_result["missing_columns"]
        unexpected_columns = schema_result["unexpected_columns"]
        type_mismatches = schema_result["type_mismatches"]

        if missing_columns:
            print("\nMissing Columns")
            for column in missing_columns:
                print(f"- {column}")

        if unexpected_columns:
            print("\nUnexpected Columns")
            for column in unexpected_columns:
                print(f"- {column}")

        if type_mismatches:
            print("\nType Mismatches")
            for column, mismatch in type_mismatches.items():
                print(
                    f"- {column}: expected {mismatch['expected']}, "
                    f"found {mismatch['actual']}"
                )


if __name__ == "__main__":
    main()