import pandas as pd


def clean_column_names(df):
    """
    Standardize column names.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-]+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )

    return df


def clean_string_columns(df):
    """
    Clean text columns by removing unnecessary whitespace
    and converting empty strings to missing values.
    """

    df = df.copy()

    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace("", pd.NA)

    return df


def convert_date_columns(df):
    """
    Convert date columns from strings to datetime format.
    Invalid dates become missing values.
    """

    df = df.copy()

    date_columns = [
        "signup_date",
        "last_purchase_date"
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


def handle_invalid_values(df):
    """
    Replace values that violate known domain rules with NaN.
    """

    df = df.copy()

    # Age should be within a realistic customer age range.
    if "age" in df.columns:
        invalid_age = (df["age"] < 18) | (df["age"] > 100)
        df.loc[invalid_age, "age"] = pd.NA

    return df


def handle_missing_values(df):
    """
    Impute missing values using column-specific strategies.
    """

    df = df.copy()

    # Numerical columns: median imputation
    numerical_columns = [
        "age",
        "total_spent",
        "satisfaction_score"
    ]

    for column in numerical_columns:
        if column in df.columns:
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value)

    # Categorical column: mode imputation
    if "gender" in df.columns:
        mode_value = df["gender"].mode()[0]
        df["gender"] = df["gender"].fillna(mode_value)

    # Domain-specific categorical imputation
    if "coupon_code" in df.columns:
        df["coupon_code"] = df["coupon_code"].fillna("NO_COUPON")

    return df


def remove_duplicates(df):
    """
    Detect and remove duplicate rows.
    """

    df = df.copy()

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows detected: {duplicate_count}")

    df = df.drop_duplicates().reset_index(drop=True)

    print(f"Duplicate rows after cleaning: {df.duplicated().sum()}")

    return df


if __name__ == "__main__":

    test_df = pd.DataFrame({
        "customer_id": [1001, 1002, 1002, 1003],
        "customer_name": ["Customer A", "Customer B", "Customer B", "Customer C"]
    })

    print("========== BEFORE DUPLICATE REMOVAL ==========")
    print(test_df)

    test_df = remove_duplicates(test_df)

    print("\n========== AFTER DUPLICATE REMOVAL ==========")
    print(test_df)