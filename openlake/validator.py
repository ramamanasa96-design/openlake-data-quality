from typing import Any

import pandas as pd


def find_missing_values(
    df: pd.DataFrame,
) -> dict[str, int]:
    """
    Find columns containing missing values.

    Args:
        df: Input pandas DataFrame.

    Returns:
        Dictionary containing column names and missing counts.
    """
    missing_counts = df.isna().sum()

    return {
        str(column): int(count)
        for column, count in missing_counts.items()
        if int(count) > 0
    }


def count_duplicate_rows(
    df: pd.DataFrame,
) -> int:
    """
    Count duplicated rows.

    Args:
        df: Input pandas DataFrame.

    Returns:
        Number of duplicated rows.
    """
    return int(df.duplicated().sum())


def get_data_types(
    df: pd.DataFrame,
) -> dict[str, str]:
    """
    Return detected data types for every column.

    Args:
        df: Input pandas DataFrame.

    Returns:
        Dictionary containing column names and data types.
    """
    return {
        str(column): str(data_type)
        for column, data_type in df.dtypes.items()
    }


def validate_schema(
    df: pd.DataFrame,
    expected_schema: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Validate DataFrame columns and data types.

    Args:
        df: Input pandas DataFrame.
        expected_schema: Optional dictionary mapping columns
            to expected data types.

    Returns:
        Schema validation results.
    """
    if expected_schema is None:
        return {
            "is_valid": True,
            "missing_columns": [],
            "unexpected_columns": [],
            "type_mismatches": {},
        }

    actual_schema = get_data_types(df)

    expected_columns = set(expected_schema)
    actual_columns = set(actual_schema)

    missing_columns = sorted(
        expected_columns - actual_columns
    )

    unexpected_columns = sorted(
        actual_columns - expected_columns
    )

    type_mismatches: dict[
        str,
        dict[str, str],
    ] = {}

    common_columns = expected_columns & actual_columns

    for column in sorted(common_columns):
        expected_type = expected_schema[column]
        actual_type = actual_schema[column]

        normalized_expected = normalize_data_type(
            expected_type
        )

        normalized_actual = normalize_data_type(
            actual_type
        )

        if normalized_expected != normalized_actual:
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


def detect_outliers(
    df: pd.DataFrame,
    z_threshold: float = 3.0,
) -> dict[str, int]:
    """
    Detect outliers in numeric columns using z-scores.

    Args:
        df: Input pandas DataFrame.
        z_threshold: Z-score threshold used to identify outliers.

    Returns:
        Dictionary containing numeric columns and outlier counts.
    """
    outlier_counts: dict[str, int] = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        series = df[column].dropna()

        if series.empty:
            outlier_counts[str(column)] = 0
            continue

        standard_deviation = float(
            series.std(ddof=0)
        )

        if standard_deviation == 0:
            outlier_counts[str(column)] = 0
            continue

        z_scores = (
            (series - series.mean()).abs()
            / standard_deviation
        )

        outlier_counts[str(column)] = int(
            (z_scores > z_threshold).sum()
        )

    return outlier_counts


def normalize_data_type(
    data_type: str,
) -> str:
    """
    Normalize related pandas and Python data type names.

    Args:
        data_type: Data type name.

    Returns:
        Normalized data type category.
    """
    normalized_type = data_type.lower()

    if normalized_type in {
        "str",
        "string",
        "object",
    }:
        return "string"

    if normalized_type.startswith("int"):
        return "integer"

    if normalized_type.startswith("float"):
        return "float"

    if "datetime" in normalized_type:
        return "datetime"

    if normalized_type in {
        "bool",
        "boolean",
    }:
        return "boolean"

    return normalized_type