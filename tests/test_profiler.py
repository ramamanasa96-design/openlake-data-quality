import pandas as pd

from openlake.profiler import (
    calculate_quality_score,
    profile_columns,
)


def sample_dataframe():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "salary": [100, 200, 300, 400],
            "name": ["Alice", "Bob", None, "David"],
        }
    )


def test_profile_columns():
    df = sample_dataframe()

    profile = profile_columns(df)

    assert "id" in profile
    assert "salary" in profile
    assert "name" in profile

    assert profile["salary"]["minimum"] == 100.0
    assert profile["salary"]["maximum"] == 400.0
    assert profile["salary"]["mean"] == 250.0
    assert profile["salary"]["median"] == 250.0


def test_quality_score():
    df = sample_dataframe()

    scores = calculate_quality_score(
        df=df,
        duplicate_rows=0,
        schema_is_valid=True,
    )

    assert scores["overall_score"] > 90
    assert scores["schema_score"] == 100
    assert scores["uniqueness_score"] == 100