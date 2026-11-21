import pandas as pd


def extract_data(
    data_dir: str = "data",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Reads raw CSV files into pandas DataFrames."""
    users_df = pd.read_csv(f"{data_dir}/Users.csv")
    movies_df = pd.read_csv(f"{data_dir}/Movies.csv")
    history_df = pd.read_csv(f"{data_dir}/WatchHistory.csv")
    return users_df, movies_df, history_df