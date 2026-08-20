import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_statistical_summary(df):
    """
    Generate descriptive statistics for numerical columns.
    """

    numerical_summary = df.describe()

    return numerical_summary


def generate_categorical_summary(df):
    """
    Generate frequency summaries for categorical columns.
    """

    categorical_columns = df.select_dtypes(include="object").columns

    summaries = {}

    for column in categorical_columns:
        summaries[column] = df[column].value_counts()

    return summaries


def generate_groupby_analysis(df):
    """
    Generate meaningful grouped summaries.
    """

    groupby_results = {}

    # Average spending by subscription type
    if {"subscription_type", "total_spent"}.issubset(df.columns):
        groupby_results["average_spending_by_subscription"] = (
            df.groupby("subscription_type")["total_spent"]
            .mean()
            .sort_values(ascending=False)
        )

    # Average lifetime value by acquisition channel
    if {"acquisition_channel", "lifetime_value"}.issubset(df.columns):
        groupby_results["average_lifetime_value_by_channel"] = (
            df.groupby("acquisition_channel")["lifetime_value"]
            .mean()
            .sort_values(ascending=False)
        )

    # Average satisfaction score by device type
    if {"device_type", "satisfaction_score"}.issubset(df.columns):
        groupby_results["average_satisfaction_by_device"] = (
            df.groupby("device_type")["satisfaction_score"]
            .mean()
            .sort_values(ascending=False)
        )

    return groupby_results


def generate_eda_charts(df, output_directory="outputs/figures"):
    """
    Generate and save EDA charts.
    """

    os.makedirs(output_directory, exist_ok=True)

    # --------------------------------------------------------
    # 1. Age Distribution
    # --------------------------------------------------------

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df["age"],
        bins=20,
        kde=True
    )

    plt.title("Customer Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        f"{output_directory}/age_distribution.png"
    )

    plt.close()


    # --------------------------------------------------------
    # 2. Total Spending Distribution
    # --------------------------------------------------------

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df["total_spent"],
        bins=30,
        kde=True
    )

    plt.title("Total Spending Distribution")
    plt.xlabel("Total Spent")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        f"{output_directory}/total_spending_distribution.png"
    )

    plt.close()


    # --------------------------------------------------------
    # 3. Subscription Type Distribution
    # --------------------------------------------------------

    plt.figure(figsize=(7, 5))

    sns.countplot(
        data=df,
        x="subscription_type"
    )

    plt.title("Customers by Subscription Type")
    plt.xlabel("Subscription Type")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        f"{output_directory}/subscription_distribution.png"
    )

    plt.close()


    # --------------------------------------------------------
    # 4. Churn Distribution
    # --------------------------------------------------------

    plt.figure(figsize=(7, 5))

    sns.countplot(
        data=df,
        x="churn"
    )

    plt.title("Customer Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    plt.savefig(
        f"{output_directory}/churn_distribution.png"
    )

    plt.close()


    # --------------------------------------------------------
    # 5. Average Spending by Subscription
    # --------------------------------------------------------

    spending_by_subscription = (
        df.groupby("subscription_type")["total_spent"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))

    spending_by_subscription.plot(
        kind="bar"
    )

    plt.title("Average Spending by Subscription Type")
    plt.xlabel("Subscription Type")
    plt.ylabel("Average Total Spent")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        f"{output_directory}/average_spending_by_subscription.png"
    )

    plt.close()


    # --------------------------------------------------------
    # 6. Correlation Heatmap
    # --------------------------------------------------------

    numerical_df = df.select_dtypes(include="number")

    correlation_matrix = numerical_df.corr()

    plt.figure(figsize=(14, 10))

    sns.heatmap(
        correlation_matrix,
        cmap="coolwarm",
        center=0
    )

    plt.title("Numerical Feature Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        f"{output_directory}/correlation_heatmap.png"
    )

    plt.close()


    print(
        f"\nEDA charts saved to: {output_directory}"
    )


if __name__ == "__main__":

    test_df = pd.DataFrame({
        "age": [22, 25, 30, 35, 40],
        "total_spent": [100, 250, 400, 600, 800],
        "subscription_type": [
            "Monthly",
            "Annual",
            "Monthly",
            "Annual",
            "Annual"
        ],
        "churn": [0, 0, 1, 0, 1]
    })

    print("Generating test EDA charts...")

    generate_eda_charts(test_df)

    print("EDA chart generation completed.")