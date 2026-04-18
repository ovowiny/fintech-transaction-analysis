"""**AVERAGE RESPONSE TIME PER PRODUCT**"""

response_time_product = df.groupby("Product")["response_time"].mean()
# NaN values ignored automatically

print("\nAverage Response Time per Product (seconds):")
print(response_time_product.sort_values())

response_time_minutes = response_time_product / 60
print("\nAverage Response Time per Product (minutes):")
print(response_time_minutes.sort_values())

# Definition:Response time = time difference between when a transaction was initiated (Tranx_Date) and when it was fulfilled (Updated Time)

# Note:
# Only transactions with valid Updated Time are considered
# Missing Updated Time values were excluded earlier to ensure accuracy


# Calculate average response time (Seconds)

# Group dataset by Product and calculate mean response time
response_time_product = df.groupby("Product")["response_time"].mean()

# Sort values in ascending order to identify fastest → slowest products
print("\nAverage Response Time per Product (in seconds):")
print(response_time_product.sort_values())


# Optional: Identify fastest and slowest product

# Fastest product (lowest response time)
fastest_product = response_time_product.idxmin()
fastest_time = response_time_product.min()

# Slowest product (highest response time)
slowest_product = response_time_product.idxmax()
slowest_time = response_time_product.max()

print(f"\nFastest Product: {fastest_product} ({fastest_time:.2f} seconds)")
print(f"Slowest Product: {slowest_product} ({slowest_time:.2f} seconds)")

# BUSINESS INTERPRETATION (INLINE COMMENT)


# Faster response time → better system efficiency and user experience
# Slower response time → potential delays due to system bottlenecks or external dependencies

# Identify products with no response time data
missing_response_products = response_time_product[response_time_product.isna()].index.tolist()

print("\nProducts with no response time data:")
print(missing_response_products)

"""**Advanced Analysis:Response Time vs Failure Rate**"""

# Objective:
# To analyze the relationship between system latency (response time) and transaction reliability (failure rate) across products

# Failure rate per product = percentage of transactions that are not successful
failure_rate_product = 1 - df.groupby("Product")["is_success"].mean()


# Create a DataFrame for easy comparison
performance_analysis = pd.DataFrame({
    "avg_response_time_sec": response_time_product,
    "failure_rate": failure_rate_product
})


# Sort by failure rate (highest problem first)
performance_analysis = performance_analysis.sort_values(by="failure_rate", ascending=False)

print("\nResponse Time vs Failure Rate by Product:")
print(performance_analysis)

# Products with both high failure rate and high response time
# (potential system bottlenecks)
high_risk = performance_analysis[
    (performance_analysis["failure_rate"] > 0.05) &
    (performance_analysis["avg_response_time_sec"].notnull())
]

print("\nHigh Risk Products (High Failure + High Response Time):")
print(high_risk)
