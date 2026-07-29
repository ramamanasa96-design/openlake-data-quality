import pandas as pd


def calculate_quality_score(
    df: pd.DataFrame,
    duplicate_rows: int,
    schema_is_valid: bool,
) -> dict[str, float]:
    """
    Calculate an overall data quality score from 0 to 100.

    Score components:
    - Completeness: 40%
    - Uniqueness: 30%
    - Schema validity: 30%
    """
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = int(df.isna().sum().sum())

    completeness_score = (
        ((total_cells - missing_cells) / total_cells) * 100
        if total_cells
        else 100.0
    )

    uniqueness_score = (
        ((df.shape[0] - duplicate_rows) / df.shape[0]) * 100
        if df.shape[0]
        else 100.0
    )

    schema_score = 100.0 if schema_is_valid else 0.0

    overall_score = (
        completeness_score * 0.40
        + uniqueness_score * 0.30
        + schema_score * 0.30
    )

    return {
        "overall_score": round(overall_score, 2),
        "completeness_score": round(completeness_score, 2),
        "uniqueness_score": round(uniqueness_score, 2),
        "schema_score": round(schema_score, 2),
    }