import pandas as pd


def find_missing_values(df: pd.DataFrame) -> dict[str, int]:
    """Return columns with missing values and their counts."""
    missing_counts = df.isna().sum()

    return {
        column: int(count)
        for column, count in missing_counts.items()
        if count > 0
    }


def count_duplicate_rows(df: pd.DataFrame) -> int:
    """Return the total number of duplicate rows."""
    return int(df.duplicated().sum())


def get_data_types(df: pd.DataFrame) -> dict[str, str]:
    """Return each column and its pandas data type."""
    return {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }
def validate_schema(
    df: pd.DataFrame,
    expected_schema: dict[str, str],
) -> dict[str, object]:
    """
    Compare a DataFrame against an expected schema.

    Returns missing columns, unexpected columns,
    data type mismatches, and the overall status.
    """
    actual_schema = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    expected_columns = set(expected_schema)
    actual_columns = set(actual_schema)

    missing_columns = sorted(expected_columns - actual_columns)
    unexpected_columns = sorted(actual_columns - expected_columns)

    type_mismatches: dict[str, dict[str, str]] = {}

    for column in expected_columns & actual_columns:
        expected_type = expected_schema[column]
        actual_type = actual_schema[column]

        if expected_type != actual_type:
            type_mismatches[column] = {
                "expected": expected_type,
                "actual": actual_type,
            }

    is_valid = not (
        missing_columns
        or unexpected_columns
        or type_mismatches
    )

    return {
        "is_valid": is_valid,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "type_mismatches": type_mismatches,
    }