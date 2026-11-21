import pandas as pd


def transform_data(
    users_df: pd.DataFrame,
    movies_df: pd.DataFrame,
    history_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merges datasets and engineers analytical features."""
    merged = history_df.merge(users_df, on="user_id", how="inner")
    merged = merged.merge(movies_df, on="movie_id", how="inner")

    if {"watch_duration_mins", "duration_mins"}.issubset(merged.columns):
        merged["completion_pct"] = (
            (merged["watch_duration_mins"] / merged["duration_mins"]) * 100
        ).clip(upper=100).round(2)

    return merged