import pandas as pd


def clean_data(
    users_df: pd.DataFrame,
    movies_df: pd.DataFrame,
    history_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Standardizes data types and handles duplicates and missing values."""
    users = users_df.drop_duplicates(subset=["user_id"]).dropna(subset=["user_id"])
    movies = movies_df.drop_duplicates(subset=["movie_id"]).dropna(
        subset=["movie_id", "title"]
    )
    history = history_df.drop_duplicates().dropna(subset=["user_id", "movie_id"])

    if "genre" in movies.columns:
        movies["genre"] = movies["genre"].fillna("Unknown")

    if "watch_duration_mins" in history.columns:
        history["watch_duration_mins"] = pd.to_numeric(
            history["watch_duration_mins"], errors="coerce"
        ).fillna(0)

    if "watch_date" in history.columns:
        history["watch_date"] = pd.to_datetime(history["watch_date"], errors="coerce")

    return users, movies, history