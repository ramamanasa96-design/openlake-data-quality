from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".json",
    ".parquet",
    ".xlsx",
    ".xls",
}


def read_dataset(file_path: str) -> pd.DataFrame:
    """
    Read a supported dataset into a pandas DataFrame.

    Supported formats:
        - CSV
        - JSON
        - Parquet
        - Excel

    Args:
        file_path: Path to the dataset.

    Returns:
        A pandas DataFrame.

    Raises:
        FileNotFoundError: If the dataset does not exist.
        ValueError: If the file type is unsupported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        supported_types = ", ".join(
            sorted(SUPPORTED_EXTENSIONS)
        )

        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: {supported_types}"
        )

    if extension == ".csv":
        return pd.read_csv(path)

    if extension == ".json":
        try:
            return pd.read_json(path)
        except ValueError:
            return pd.read_json(
                path,
                lines=True,
            )

    if extension == ".parquet":
        return pd.read_parquet(path)

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(
        f"Unable to read file: {file_path}"
    )