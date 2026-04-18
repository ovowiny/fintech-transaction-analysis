"""**DAILY TREND FOR TOP 5 CUSTOMERS**"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
# Objective: To analyze transaction trends over time for the top 5 customers
# This helps understand customer behavior, consistency, and dependency risk

# Identify top 5 Customers

# Top customers are determined based on total transaction value (Amount)
top_customers = (
    df.groupby("Customer ID")["Amount"].sum().sort_values(ascending=False)
    .head(5).index
)

print("\nTop 5 Customers:")
print(top_customers)


# Keep only transactions belonging to the top 5 customers
df_top = df[df["Customer ID"].isin(top_customers)]

# Aggregate transaction value by date and customer. This gives daily spending trend per customer
daily_trend = (
    df_top.groupby(["date", "Customer ID"])["Amount"].sum().reset_index()
)

print("\nSample of Daily Trend Data:")
print(daily_trend.head())

# Plot line chart for each customer
# Each line represents a customer's daily transaction value

for cust in top_customers:
    customer_data = daily_trend[daily_trend["Customer ID"] == cust]

    plt.plot(
        customer_data["date"],
        customer_data["Amount"],
        marker='o',
        label=f"{cust}"
    )

    # Annotate ONLY last point (cleaner)
    last_x = customer_data["date"].iloc[-1]
    last_y = customer_data["Amount"].iloc[-1]

    plt.text(
        last_x, last_y,
        f"{last_y/1e6:.1f}M",
        fontsize=9,
        ha='left'
    )

# Formatting
plt.title("Daily Transaction Trend for Top 5 Customers")
plt.xlabel("Date")
plt.ylabel("Transaction Value (₦)")
plt.xticks(rotation=45)
plt.legend(title="Customer ID")
plt.tight_layout()

plt.show()
plt.savefig("top5_customers_trend_clean.png")
plt.clf()

# Addtional Analysis: Identify most consistent vs most volatile customer

# Calculate daily standard deviation per customer
volatility = (
    daily_trend.groupby("Customer ID")["Amount"]
    .std().sort_values(ascending=False)
)

print("\nCustomer Volatility (Std Dev of Daily Spend):")
print(volatility)

# Interpretation:
# Higher std = more fluctuation (less predictable)
# Lower std = more stable behavior

"""**LEAST PERFORMING CUSTOMERS PER PRODUCT**"""

# Objective: Identify the bottom 10 customers per product based on performance

# Definition of "least performing": - Low total transaction value (Amount) & High failure rate
# This helps detect customers contributing little value and/or experiencing issues

# Aggregate customer performance per product

# Group by Product and Customer ID
performance = df.groupby(["Product", "Customer ID"]).agg({
    "Amount": "sum",        # Total transaction value per customer per product
    "is_success": "mean"    # Success rate (mean of True/False)
}).reset_index()

# Calculate failure rate

# Failure rate = 1 - success rate
performance["failure_rate"] = 1 - performance["is_success"]


# Define Performance Score

# Create a combined metric to rank customers: Lower Amount + Higher Failure Rate = Worse performance

# Normalize Amount (to bring to same scale)
performance["normalized_amount"] = performance["Amount"] / performance["Amount"].max()

# Performance score (lower is worse)
performance["performance_score"] = (
    performance["normalized_amount"] * performance["is_success"]
)

# Identify least Perfoming Customers

# Sort:
# - Lowest Amount first
# - Highest failure rate first

least_performing = (
    performance
    .sort_values(
        by=["Product", "Amount", "failure_rate"],
        ascending=[True, True, False]
    )
    .groupby("Product")
    .head(10)   # Bottom 10 per product
)

print("\nLeast Performing Customers per Product:")
print(least_performing)

# OPTIONAL — FOCUS ON CRITICAL CASES

# Customers with high failure rate (> 10%)
high_failure_customers = performance[performance["failure_rate"] > 0.1]

print("\nCustomers with High Failure Rate (>10%):")
print(high_failure_customers.sort_values(by="failure_rate", ascending=False))

least_performing.to_csv("least_performing_customers.csv", index=False)

# files.download("least_performing_customers.csv")

"""**CUSTOMER SUMMARY TABLE**"""

# Objective: Build a comprehensive customer-level summary table
# capturing performance, revenue contribution, and failure behavior

# Total Transaction Value (for % contribution)
total_value = df["Amount"].sum()

# Product Failure Rate 
def product_failure_rate(product_name):
    subset = df[df["Product"] == product_name]
    rate = subset.groupby("Customer ID")["is_success"].mean()
    return 1 - rate

customer_summary = (
    df.groupby("Customer ID").agg(
        successful_facevalue=("Amount", lambda x: x[df.loc[x.index, "is_success"]].sum()),
        failed_facevalue=("Amount", lambda x: x[~df.loc[x.index, "is_success"]].sum()),
        estimated_profit=("profit", lambda x: x[df.loc[x.index, "is_success"]].sum()),
        total_value=("Amount", "sum"),
        successful_count=("is_success", "sum"),
        total_count=("is_success", "count")
    )
    .reset_index()
)

# Value contribution
customer_summary["value_contribution_pct"] = (
    customer_summary["total_value"] / total_value * 100
)

# Failure rate
customer_summary["failure_rate"] = (
    1 - (customer_summary["successful_count"] / customer_summary["total_count"])
)

# Product-level failure rates
customer_summary["airtime_failure_rate"] = customer_summary["Customer ID"].map(product_failure_rate("airtime"))
customer_summary["data_failure_rate"] = customer_summary["Customer ID"].map(product_failure_rate("data"))
customer_summary["cabletv_failure_rate"] = customer_summary["Customer ID"].map(product_failure_rate("cabletv"))
customer_summary["electricity_failure_rate"] = customer_summary["Customer ID"].map(product_failure_rate("electricity"))

# Fill missing values
customer_summary = customer_summary.fillna(0)

# Sort
customer_summary = customer_summary.sort_values(by="total_value", ascending=False)

# Output
print(customer_summary.head(10))
customer_summary.to_csv("customer_summary.csv", index=False)
