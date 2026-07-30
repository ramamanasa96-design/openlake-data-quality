from typing import Any

import pandas as pd


def calculate_quality_score(
    df: pd.DataFrame,
    duplicate_rows: int,
    schema_is_valid: bool,
) -> dict[str, float]:
    """
    Calculate overall data quality scores.
    """
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = int(df.isna().sum().sum())

    completeness_score = (
        100.0
        if total_cells == 0
        else ((total_cells - missing_cells) / total_cells) * 100
    )

    uniqueness_score = (
        100.0
        if len(df) == 0
        else ((len(df) - duplicate_rows) / len(df)) * 100
    )

    schema_score = 100.0 if schema_is_valid else 0.0

    overall_score = (
        completeness_score
        + uniqueness_score
        + schema_score
    ) / 3

    return {
        "overall_score": round(overall_score, 2),
        "completeness_score": round(completeness_score, 2),
        "uniqueness_score": round(uniqueness_score, 2),
        "schema_score": round(schema_score, 2),
    }


def profile_columns(
    df: pd.DataFrame,
) -> dict[str, dict[str, Any]]:
    """
    Generate detailed profile information for each column.
    """
    profile: dict[str, dict[str, Any]] = {}

    for column in df.columns:
        series = df[column]

        column_profile: dict[str, Any] = {
            "data_type": str(series.dtype),
            "non_null_count": int(series.notna().sum()),
            "missing_count": int(series.isna().sum()),
            "unique_count": int(series.nunique(dropna=True)),
        }

        if pd.api.types.is_numeric_dtype(series):
            numeric = series.dropna()

            if numeric.empty:
                column_profile.update(
                    {
                        "minimum": None,
                        "maximum": None,
                        "mean": None,
                        "median": None,
                    }
                )
            else:
                column_profile.update(
                    {
                        "minimum": float(numeric.min()),
                        "maximum": float(numeric.max()),
                        "mean": round(float(numeric.mean()), 2),
                        "median": round(float(numeric.median()), 2),
                    }
                )

        profile[str(column)] = column_profile

    return profile