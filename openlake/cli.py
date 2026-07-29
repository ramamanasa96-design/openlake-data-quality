from openlake.reader import read_dataset
from openlake.validator import (
    count_duplicate_rows,
    find_missing_values,
    get_data_types,
)


def main() -> None:
    df = read_dataset("sample_data/employees.csv")

    missing_values = find_missing_values(df)
    duplicate_rows = count_duplicate_rows(df)
    data_types = get_data_types(df)

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


if __name__ == "__main__":
    main()