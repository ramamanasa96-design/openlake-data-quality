from openlake.reader import read_dataset


def main():

    df = read_dataset("sample_data/employees.csv")

    print("=" * 50)
    print("OpenLake Data Quality Framework")
    print("=" * 50)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names")
    print(list(df.columns))

    print("\nDataset Preview")
    print(df.head())


if __name__ == "__main__":
    main()