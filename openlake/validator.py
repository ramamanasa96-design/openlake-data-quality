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