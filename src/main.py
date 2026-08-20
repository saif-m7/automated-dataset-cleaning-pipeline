import os

import pandas as pd

from cleaning import (
    clean_column_names,
    clean_string_columns,
    convert_date_columns,
    handle_invalid_values,
    handle_missing_values,
    remove_duplicates
)

from eda import (
    generate_statistical_summary,
    generate_categorical_summary,
    generate_groupby_analysis,
    generate_eda_charts
)


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = "data/raw/Sales - Marketing customer dataset.csv"
OUTPUT_FILE = "data/processed/cleaned_dataset.csv"

REPORT_DIRECTORY = "outputs/reports"
FIGURE_DIRECTORY = "outputs/figures"


# ============================================================
# Load Dataset
# ============================================================

def load_data(file_path):
    """
    Load the raw CSV dataset.
    """

    print("\n========== LOADING DATASET ==========")

    df = pd.read_csv(file_path)

    print("Dataset loaded successfully.")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    return df


# ============================================================
# Generate Data Quality Profile
# ============================================================

def generate_profile(df):
    """
    Generate basic data-quality statistics.
    """

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    }

    return profile


# ============================================================
# Cleaning Pipeline
# ============================================================

def clean_dataset(df):
    """
    Execute the complete automated cleaning pipeline.
    """

    print("\n========== STARTING CLEANING PIPELINE ==========")

    print("\n1. Cleaning column names...")
    df = clean_column_names(df)

    print("2. Cleaning string values...")
    df = clean_string_columns(df)

    print("3. Converting date columns...")
    df = convert_date_columns(df)

    print("4. Handling invalid values...")
    df = handle_invalid_values(df)

    print("5. Handling missing values...")
    df = handle_missing_values(df)

    print("6. Removing duplicates...")
    df = remove_duplicates(df)

    print("\n========== CLEANING PIPELINE COMPLETE ==========")

    return df


# ============================================================
# Save Cleaning Report
# ============================================================

def save_cleaning_report(before, after):
    """
    Save before-vs-after cleaning statistics.
    """

    os.makedirs(REPORT_DIRECTORY, exist_ok=True)

    report = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows"
        ],
        "Before Cleaning": [
            before["rows"],
            before["columns"],
            before["missing_values"],
            before["duplicate_rows"]
        ],
        "After Cleaning": [
            after["rows"],
            after["columns"],
            after["missing_values"],
            after["duplicate_rows"]
        ]
    })

    report_path = f"{REPORT_DIRECTORY}/cleaning_summary.csv"

    report.to_csv(report_path, index=False)

    print(f"\nCleaning report saved to: {report_path}")


# ============================================================
# Save EDA Results
# ============================================================

def save_eda_results(df):
    """
    Generate and save EDA statistics and analyses.
    """

    os.makedirs(REPORT_DIRECTORY, exist_ok=True)

    # --------------------------------------------------------
    # Statistical Summary
    # --------------------------------------------------------

    statistical_summary = generate_statistical_summary(df)

    statistical_summary.to_csv(
        f"{REPORT_DIRECTORY}/statistical_summary.csv"
    )

    # --------------------------------------------------------
    # Categorical Summary
    # --------------------------------------------------------

    categorical_results = generate_categorical_summary(df)

    for column, result in categorical_results.items():

        result.to_csv(
            f"{REPORT_DIRECTORY}/category_{column}.csv"
        )

    # --------------------------------------------------------
    # Groupby Analysis
    # --------------------------------------------------------

    groupby_results = generate_groupby_analysis(df)

    for name, result in groupby_results.items():

        result.to_csv(
            f"{REPORT_DIRECTORY}/{name}.csv"
        )

    print("\nEDA reports saved successfully.")


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. Load raw dataset
    # --------------------------------------------------------

    df = load_data(INPUT_FILE)

    # --------------------------------------------------------
    # 2. Profile before cleaning
    # --------------------------------------------------------

    before = generate_profile(df)

    print("\n========== BEFORE CLEANING ==========")
    print(f"Rows: {before['rows']}")
    print(f"Columns: {before['columns']}")
    print(f"Missing values: {before['missing_values']}")
    print(f"Duplicate rows: {before['duplicate_rows']}")

    # --------------------------------------------------------
    # 3. Clean dataset
    # --------------------------------------------------------

    cleaned_df = clean_dataset(df)

    # --------------------------------------------------------
    # 4. Profile after cleaning
    # --------------------------------------------------------

    after = generate_profile(cleaned_df)

    print("\n========== AFTER CLEANING ==========")
    print(f"Rows: {after['rows']}")
    print(f"Columns: {after['columns']}")
    print(f"Missing values: {after['missing_values']}")
    print(f"Duplicate rows: {after['duplicate_rows']}")

    # --------------------------------------------------------
    # 5. Save cleaned dataset
    # --------------------------------------------------------

    os.makedirs("data/processed", exist_ok=True)

    cleaned_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nCleaned dataset saved successfully.")
    print(f"File: {OUTPUT_FILE}")

    # --------------------------------------------------------
    # 6. Save before-vs-after report
    # --------------------------------------------------------

    save_cleaning_report(
        before,
        after
    )

    # --------------------------------------------------------
    # 7. Generate EDA reports
    # --------------------------------------------------------

    print("\n========== GENERATING EDA ==========")

    statistical_summary = generate_statistical_summary(
        cleaned_df
    )

    print("\nStatistical summary:")
    print(statistical_summary)

    print("\nGenerating categorical summaries...")

    categorical_results = generate_categorical_summary(
        cleaned_df
    )

    for column, result in categorical_results.items():

        print(f"\n{column}:")
        print(result)

    print("\n========== GROUPBY ANALYSIS ==========")

    groupby_results = generate_groupby_analysis(
        cleaned_df
    )

    for name, result in groupby_results.items():

        print(f"\n{name}:")
        print(result)

    # --------------------------------------------------------
    # 8. Save EDA reports
    # --------------------------------------------------------

    save_eda_results(
        cleaned_df
    )

    # --------------------------------------------------------
    # 9. Generate EDA charts
    # --------------------------------------------------------

    print("\n========== GENERATING EDA CHARTS ==========")

    generate_eda_charts(
        cleaned_df,
        FIGURE_DIRECTORY
    )

    print("\n========== COMPLETE PIPELINE FINISHED ==========")


if __name__ == "__main__":
    main()