import pandas as pd
import pytest

from openlake.reader import read_dataset


def test_read_csv():
    df = read_dataset("sample_data/employees.csv")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_invalid_file():
    with pytest.raises(FileNotFoundError):
        read_dataset("sample_data/not_found.csv")


def test_unsupported_extension(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello")

    with pytest.raises(ValueError):
        read_dataset(str(file_path))