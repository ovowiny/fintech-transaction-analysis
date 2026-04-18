"""
Importing the necessary librabries needed for the analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

"""Loading the Dataset"""

# Load dataset containing transaction records from my drive
df = pd.read_csv("/content/drive/MyDrive/Dataset.csv")

"""## Data Inspection and Cleaning

### Basic info: number of rows, columns, data types, non-null counts
"""

# Preview dataset
print("First 5 rows:")
df.head()

#To check the number of rows and columns in the dataset
df.shape

print("\nDataset Info:")
df.info()

# Rename product column for consistency with description
df.rename(columns={"product": "Product"}, inplace=True)

# Convert Customer ID to string (IDs are identifiers, not numeric)
df["Customer ID"] = df["Customer ID"].astype(str)

# Convert Tranx_Date and Updated Time to datetime objects for time calculations
df["Tranx_Date"] = pd.to_datetime(df["Tranx_Date"], errors='coerce')
df["Updated Time"] = pd.to_datetime(df["Updated Time"], errors='coerce')

print("\nDataset Info:")
df.info()

"""Check for Missing Values and Handling"""

# Checking for the number of missing values for each column
print("\nMissing values per column:\n", df.isnull().sum())

# Fill minor missing categorical column
df["Vending Channel"] = df["Vending Channel"].fillna("Unknown")

# Checking for missing values for each column after handling
print("\nMissing values per column:\n", df.isnull().sum())

"""Out of 5,195 transactions missing Updated Time, 4,475 were successful.
For integrity of response time metrics, these rows were excluded only from calculations requiring timestamp data.
All other analyses (revenue, profit, success rate) include these transactions to prevent bias and preserve accurate business insights.”

### Duplicates and Standardization
"""

# Count duplicate rows
duplicates = df.duplicated().sum()
print(f"Duplicates: {duplicates}")

"""The dataset do not contain duplicates"""

# Standardize categorical fields

# Removes any leading or trailing spaces from the text in the "Status" column
df["Status"] = df["Status"].str.strip()

# Converts all text in the "Product" column to lowercase
df["Product"] = df["Product"].str.lower()

"""### **Feature Engineering**"""

# Calculate profit per transaction
df["profit"] = df["Amount"] - df["Buying Price"]

# Create flag for successful transactions
df["is_success"] = df["Status"] == "Successful"

# Calculate response time (seconds) only for transactions with Updated Time
df["response_time"] = np.where(
    df["Updated Time"].notnull(),
    (df["Updated Time"] - df["Tranx_Date"]).dt.total_seconds(),
    np.nan
)

# Extract date for trend analysis
df["date"] = df["Tranx_Date"].dt.date
df["hour"] = df["Tranx_Date"].dt.hour

df.head()
