import os
import pandas as pd


def load_and_report(
    transformed_df: pd.DataFrame,
    metrics: dict,
    output_dir: str = "output",
) -> None:
    """Saves the warehouse table, CSV reports, and prints a detailed executive summary."""
    os.makedirs(output_dir, exist_ok=True)
    transformed_df.to_csv(f"{output_dir}/netflix_warehouse.csv", index=False)

    for report_name, item in metrics.items():
        if isinstance(item, pd.DataFrame):
            item.to_csv(f"{output_dir}/{report_name}.csv", index=False)

    ov = metrics["overview"]
    lines = [
        "=" * 65,
        "              NETFLIX ETL PIPELINE - EXECUTIVE SUMMARY",
        "=" * 65,
    ]
    if "date_start" in ov:
        lines.append(f"Reporting Period       : {ov['date_start']} to {ov['date_end']}")
    lines.extend(
        [
            f"Total Watch Sessions   : {ov['total_sessions']}",
            f"Unique Active Users    : {ov['unique_users']}",
            f"Unique Titles Watched  : {ov['unique_movies']}",
            f"Total Watch Time       : {ov['total_watch_mins']:,.0f} mins ({ov['total_watch_hours']:.2f} hrs)",
            f"Avg / Median Session   : {ov['avg_watch_mins']:.2f} mins / {ov['median_watch_mins']:.2f} mins",
            f"Avg Completion Rate    : {ov['avg_completion_pct']:.2f}% ({ov['completed_sessions']}/{ov['total_sessions']} sessions >= 90%)",
            "",
            "--- TOP WATCHED TITLES ---",
            metrics["top_movies"].to_string(index=False),
            "",
            "--- GENRE PERFORMANCE ---",
            metrics["genre_stats"].to_string(index=False),
        ]
    )

    if "plan_stats" in metrics:
        lines.extend(
            [
                "",
                "--- SUBSCRIPTION PLAN BREAKDOWN ---",
                metrics["plan_stats"].to_string(index=False),
            ]
        )

    if "top_users" in metrics:
        lines.extend(
            [
                "",
                "--- TOP 5 MOST ACTIVE USERS ---",
                metrics["top_users"].to_string(index=False),
            ]
        )

    if "country_stats" in metrics:
        lines.extend(
            [
                "",
                "--- ENGAGEMENT BY COUNTRY ---",
                metrics["country_stats"].to_string(index=False),
            ]
        )

    lines.append("=" * 65)
    report_text = "\n".join(lines)

    with open(f"{output_dir}/executive_summary.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("\n" + report_text)