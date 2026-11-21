from extract import extract_data
from clean import clean_data
from transform import transform_data
from analysis import analyze_data
from report import load_and_report


def run_pipeline() -> None:
    print("1. Extracting raw CSV files...")
    users_raw, movies_raw, history_raw = extract_data(data_dir="data")

    print("2. Cleaning datasets...")
    users_clean, movies_clean, history_clean = clean_data(
        users_raw, movies_raw, history_raw
    )

    print("3. Transforming and joining tables...")
    warehouse_df = transform_data(users_clean, movies_clean, history_clean)

    print("4. Analyzing watch metrics...")
    metrics = analyze_data(warehouse_df)

    print("5. Loading data and generating reports...")
    load_and_report(warehouse_df, metrics, output_dir="output")

    print("\nETL Pipeline finished successfully.")


if __name__ == "__main__":
    run_pipeline()