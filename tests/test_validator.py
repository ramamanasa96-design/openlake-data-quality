import pandas as pd

from openlake.validator import (
    count_duplicate_rows,
    detect_outliers,
    find_missing_values,
    get_data_types,
    validate_schema,
)


def sample_dataframe():
    return pd.DataFrame(
        {
            "id": [1, 2, 2, 4],
            "name": ["Alice", "Bob", "Bob", None],
            "salary": [50000, 60000, 60000, 999999],
        }
    )


def test_find_missing_values():
    df = sample_dataframe()

    result = find_missing_values(df)

    assert result == {
        "name": 1,
    }


def test_duplicate_rows():
    df = sample_dataframe()

    duplicates = count_duplicate_rows(df)

    assert duplicates == 1


def test_get_data_types():
    df = sample_dataframe()

    data_types = get_data_types(df)

    assert data_types["id"] == "int64"
    assert data_types["salary"] == "int64"


def test_validate_schema_pass():
    df = sample_dataframe()

    schema = {
        "id": "int64",
        "name": "object",
        "salary": "int64",
    }

    result = validate_schema(df, schema)

    assert result["is_valid"] is True


def test_validate_schema_fail():
    df = sample_dataframe()

    schema = {
        "id": "int64",
        "name": "object",
        "salary": "float64",
    }

    result = validate_schema(df, schema)

    assert result["is_valid"] is False
    assert "salary" in result["type_mismatches"]


def test_detect_outliers():
    df = sample_dataframe()

    outliers = detect_outliers(df)

    assert "salary" in outliers