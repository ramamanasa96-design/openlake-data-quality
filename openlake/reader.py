from pathlib import Path
import pandas as pd


def read_dataset(file_path: str) -> pd.DataFrame:
    """
    Reads CSV, JSON, or Parquet files.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    extension = path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(path)

    elif extension == ".json":
        return pd.read_json(path)

    elif extension == ".parquet":
        return pd.read_parquet(path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )