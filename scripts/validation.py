print("\n--- DATA VALIDATION ---")

# Critical columns should have no missing values
critical_cols = ["Customer ID", "Amount", "Tranx_Date", "Product", "Status"]
for col in critical_cols:
    null_count = df[col].isnull().sum()
    print(f"{col} nulls: {null_count}")
    # Raise error if critical column has missing values
    assert null_count == 0, f"{col} has missing values!"

# Ensure Amount column is positive
invalid_amount = df[df["Amount"] <= 0].shape[0]
print(f"Invalid amount rows: {invalid_amount}")
assert invalid_amount == 0, "Amount contains zero or negative values!"

# Check that Status only contains valid values
valid_status = ["Successful", "Too much requests/System too Busy", "Wrong Product", "Other Errors", "Validation Error"]
invalid_status = df[~df["Status"].isin(valid_status)].shape[0]
print(f"Invalid status rows: {invalid_status}")
assert invalid_status == 0, "Unexpected status values found!"

# Confirm duplicates removed after cleaning
duplicates_check = df.duplicated().sum()
assert duplicates_check == 0, "Duplicates exist after cleaning!"

# Check for extreme losses (optional sanity check)
extreme_loss = df[df["profit"] < -10000].shape[0]
print(f"Extreme loss transactions: {extreme_loss}")

print("--- DATA VALIDATION COMPLETED ---\n")
