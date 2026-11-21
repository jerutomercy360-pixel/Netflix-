import pandas as pd


def analyze_data(df: pd.DataFrame) -> dict:
    """Computes KPIs and multi-dimensional aggregations from the transformed dataset."""
    total_mins = float(df["watch_duration_mins"].sum())
    completed_count = (
        int((df["completion_pct"] >= 90).sum()) if "completion_pct" in df.columns else 0
    )

    overview = {
        "total_sessions": int(len(df)),
        "unique_users": int(df["user_id"].nunique()),
        "unique_movies": int(df["movie_id"].nunique()),
        "total_watch_mins": round(total_mins, 2),
        "total_watch_hours": round(total_mins / 60, 2),
        "avg_watch_mins": round(float(df["watch_duration_mins"].mean()), 2),
        "median_watch_mins": round(float(df["watch_duration_mins"].median()), 2),
        "avg_completion_pct": (
            round(float(df["completion_pct"].mean()), 2)
            if "completion_pct" in df.columns
            else 0.0
        ),
        "completed_sessions": completed_count,
    }

    if "watch_date" in df.columns and df["watch_date"].notna().any():
        overview["date_start"] = df["watch_date"].min().strftime("%Y-%m-%d")
        overview["date_end"] = df["watch_date"].max().strftime("%Y-%m-%d")

    top_movies = (
        df.groupby(["title", "genre"], as_index=False)
        .agg(
            total_views=("movie_id", "count"),
            total_watch_mins=("watch_duration_mins", "sum"),
            avg_completion_pct=("completion_pct", "mean"),
        )
        .sort_values(by=["total_watch_mins", "total_views"], ascending=False)
        .head(10)
        .round(2)
    )

    genre_stats = (
        df.groupby("genre", as_index=False)
        .agg(
            total_views=("movie_id", "count"),
            total_watch_mins=("watch_duration_mins", "sum"),
            avg_watch_mins=("watch_duration_mins", "mean"),
            avg_completion_pct=("completion_pct", "mean"),
        )
        .sort_values(by="total_watch_mins", ascending=False)
        .round(2)
    )

    results = {
        "overview": overview,
        "top_movies": top_movies,
        "genre_stats": genre_stats,
    }

    if "subscription_plan" in df.columns:
        results["plan_stats"] = (
            df.groupby("subscription_plan", as_index=False)
            .agg(
                active_users=("user_id", "nunique"),
                total_views=(
                    "watch_id" if "watch_id" in df.columns else "movie_id",
                    "count",
                ),
                total_watch_mins=("watch_duration_mins", "sum"),
                avg_watch_mins=("watch_duration_mins", "mean"),
            )
            .sort_values(by="total_watch_mins", ascending=False)
            .round(2)
        )

    if {"user_id", "name"}.issubset(df.columns):
        group_cols = [
            c
            for c in ["user_id", "name", "country", "subscription_plan"]
            if c in df.columns
        ]
        results["top_users"] = (
            df.groupby(group_cols, as_index=False)
            .agg(
                movies_watched=("movie_id", "count"),
                total_watch_mins=("watch_duration_mins", "sum"),
                avg_completion_pct=("completion_pct", "mean"),
            )
            .sort_values(by="total_watch_mins", ascending=False)
            .head(5)
            .round(2)
        )

    if "country" in df.columns:
        results["country_stats"] = (
            df.groupby("country", as_index=False)
            .agg(
                active_users=("user_id", "nunique"),
                total_views=("movie_id", "count"),
                total_watch_mins=("watch_duration_mins", "sum"),
            )
            .sort_values(by="total_watch_mins", ascending=False)
            .round(2)
        )

    return results