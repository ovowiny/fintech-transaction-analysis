"""**KPI CALCULATIONS**"""

# 1. TOTAL REVENUE
# Definition:Total revenue represents the total value of all transactions processed.
# This is a key business metric used to measure overall sales performance.

total_revenue = df["Amount"].sum()
print(f"Total Revenue: ₦{total_revenue:,.2f}")

# Business Reason: Helps understand the scale of transactions and overall business volume.


# 2. TOTAL PROFIT
# Definition:Profit is calculated as the difference between selling price (Amount) and cost price (Buying Price) for each transaction.

total_profit = df["profit"].sum()
print(f"Total Profit: ₦{total_profit:,.2f}")

# Business Reason: Indicates how much the company is actually earning after costs. Revenue alone is not enough — profitability is key.


# 3. PROFIT MARGIN
# Definition: Profit margin shows how much profit is generated per unit of revenue.

profit_margin = total_profit / total_revenue
print(f"Profit Margin: {profit_margin:.2%}")

# Business Reason: Measures efficiency of pricing and cost control. Low margin may indicate high supplier cost or pricing inefficiencies.


# 4. SUCCESS RATE
# Definition: Percentage of transactions that were successful.

success_rate = df["is_success"].mean()
print(f"Success Rate: {success_rate:.2%}")

# Business Reason: Indicates system reliability and operational performance.
# Higher success rate = better customer experience and higher revenue retention.


# 5. FAILURE RATE
# Definition: Percentage of transactions that failed.

failure_rate = 1 - success_rate
print(f"Failure Rate: {failure_rate:.2%}")

# Business Reason: Represents lost revenue opportunities and system inefficiencies.
# Reducing failure rate directly improves business performance.


# 6. PRODUCT PERFORMANCE
# Definition: Evaluate how each product contributes to revenue, profit, and success rate.

product_perf = df.groupby("Product").agg({
    "Amount": "sum",        # Total revenue per product
    "profit": "sum",        # Total profit per product
    "is_success": "mean"    # Success rate per product
}).rename(columns={"is_success": "success_rate"})

print("\nProduct Performance:")
print(product_perf.sort_values("Amount", ascending=False))

# Business Reason:
# Helps identify:
# - Top revenue-generating products
# - Most profitable products
# - Products with high failure rates (operational issues)

# 7. TOTAL CUSTOMERS
# Total number of unique customers
total_customers = df["Customer ID"].nunique()

# Print to confirm
print(f"Total Customers: {total_customers}")
# Business Reason: Provides context on the size of the customer base.
# It also helps assess revenue concentration and dependency risk.


# 8. CUSTOMER CONTRIBUTION
# Definition: Measures how much each customer contributes to total revenue.

customer_revenue = df.groupby("Customer ID")["Amount"].sum().sort_values(ascending=False)

# Calculate top 5 contribution
top5_contribution = customer_revenue.head(5).sum() / customer_revenue.sum()

print(f"\nTop 5 Customers Contribution: {top5_contribution:.2%}")

# Display top customers
print("\nTop 10 Customers by Revenue:")
print(customer_revenue.head(10))

# Business Reason: Identifies key customers driving the business.
# Helps detect dependency risk if revenue is concentrated among few customers.


# ADDITIONAL KPI
# 9. Average transaction value

avg_transaction_value = df["Amount"].mean()
print(f"\nAverage Transaction Value: ₦{avg_transaction_value:,.2f}")

# Business Reason: Helps understand customer spending behavior.
# Useful for pricing strategy and segmentation.


# 10. FAILURE RATE BY PRODUCT
failure_by_product = df.groupby("Product")["is_success"].mean()
failure_by_product = 1 - failure_by_product

print("\nFailure Rate by Product:")
print(failure_by_product.sort_values(ascending=False))

# Business Reason: Identifies problematic products causing failures.
# Helps prioritize operational improvements.
