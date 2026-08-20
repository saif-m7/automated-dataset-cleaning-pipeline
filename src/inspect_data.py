import pandas as pd

# Load the raw dataset
file_path = "data/raw/Sales - Marketing customer dataset.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print(df.duplicated().sum())

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all"))

print("\n========== UNIQUE CATEGORICAL VALUES ==========")

categorical_columns = [
    "gender",
    "country",
    "city",
    "acquisition_channel",
    "device_type",
    "subscription_type",
    "payment_method"
]

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False))


print("\n========== NUMERICAL RANGES ==========")

numerical_columns = df.select_dtypes(include="number").columns

for column in numerical_columns:
    print(f"\n{column}:")
    print(f"Min: {df[column].min()}")
    print(f"Max: {df[column].max()}")