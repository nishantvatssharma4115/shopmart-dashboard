# ============================================================
# generate_data.py
# Purpose: Generate, clean, and summarize a fake e-commerce
#          sales dataset using only NumPy, Pandas, and Random.
# ============================================================

import numpy as np          # Import NumPy for numerical operations and array handling
import pandas as pd          # Import Pandas for DataFrame creation and data manipulation
import random                # Import Random for generating random choices and numbers

# ── 1. SET RANDOM SEEDS FOR REPRODUCIBILITY ─────────────────
# Setting seeds ensures we get the same "random" data every time we run the script
random.seed(42)              # Fix Python's built-in random seed to 42
np.random.seed(42)           # Fix NumPy's random seed to 42

# ── 2. DEFINE THE NUMBER OF ROWS ────────────────────────────
n_rows = 300                 # We want exactly 300 records in our dataset

# ── 3. DEFINE POSSIBLE VALUES FOR CATEGORICAL COLUMNS ───────
regions = ["North", "South", "East", "West"]                              # Four geographic sales regions
categories = ["Electronics", "Clothing", "Food", "Beauty", "Sports"]      # Five product categories

# Map each category to realistic product names so our data feels authentic
product_map = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],   # Electronics products
    "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers"],              # Clothing products
    "Food":        ["Protein Bar", "Green Tea", "Almonds", "Honey", "Oats"],         # Food products
    "Beauty":      ["Face Wash", "Moisturizer", "Lipstick", "Serum", "Sunscreen"],   # Beauty products
    "Sports":      ["Yoga Mat", "Dumbbells", "Resistance Band", "Skipping Rope", "Water Bottle"],  # Sports products
}

customer_segments = ["New", "Returning", "VIP"]    # Three types of customers based on purchase history

# ── 4. GENERATE RANDOM DATA FOR EACH COLUMN ─────────────────

# Generate 300 unique Order IDs in the format ORD-0001, ORD-0002, ... ORD-0300
order_ids = [f"ORD-{str(i).zfill(4)}" for i in range(1, n_rows + 1)]

# Generate 300 random dates between 2023-01-01 and 2023-12-31
start_date = pd.Timestamp("2023-01-01")                                     # Set the earliest possible date
end_date   = pd.Timestamp("2023-12-31")                                     # Set the latest possible date
date_range_days = (end_date - start_date).days                              # Calculate the total number of days in our range (364)
random_days = np.random.randint(0, date_range_days + 1, size=n_rows)        # Pick 300 random offsets (in days)
dates = [start_date + pd.Timedelta(days=int(d)) for d in random_days]      # Add each offset to the start date to get final dates

# Randomly pick a region for each of the 300 orders
selected_regions = [random.choice(regions) for _ in range(n_rows)]

# Randomly pick a product category for each order
selected_categories = [random.choice(categories) for _ in range(n_rows)]

# Pick a product name that matches the chosen category for each order
selected_products = [random.choice(product_map[cat]) for cat in selected_categories]

# Generate random units sold between 1 and 50 for each order
units_sold = np.random.randint(1, 51, size=n_rows)

# Generate random unit prices between $5.00 and $999.99, rounded to 2 decimal places
unit_prices = np.round(np.random.uniform(5.0, 999.99, size=n_rows), 2)

# Generate random discount percentages between 0% and 40%, rounded to 1 decimal place
discount_percents = np.round(np.random.uniform(0, 40, size=n_rows), 1)

# Randomly assign a customer segment to each order
selected_segments = [random.choice(customer_segments) for _ in range(n_rows)]

# ── 5. ASSEMBLE ALL COLUMNS INTO A PANDAS DATAFRAME ─────────
df = pd.DataFrame({
    "Order ID":           order_ids,          # Unique identifier for each order
    "Date":               dates,              # Date the order was placed
    "Region":             selected_regions,   # Geographic region of the order
    "Product Category":   selected_categories,# High-level product category
    "Product Name":       selected_products,  # Specific product purchased
    "Units Sold":         units_sold,         # How many units were sold
    "Unit Price":         unit_prices,        # Price per single unit (in USD)
    "Discount Percent":   discount_percents,  # Discount applied to the order (%)
    "Customer Segment":   selected_segments,  # Type of customer who placed the order
})

# ── 6. ARTIFICIALLY INJECT SOME MISSING VALUES (to simulate real-world mess) ──
# We randomly set ~3% of Unit Price values to NaN (missing)
missing_price_idx = np.random.choice(df.index, size=9, replace=False)   # Pick 9 random row indices
df.loc[missing_price_idx, "Unit Price"] = np.nan                         # Replace those Unit Price values with NaN

# We randomly set ~2% of Discount Percent values to NaN (missing)
missing_disc_idx = np.random.choice(df.index, size=6, replace=False)    # Pick 6 random row indices
df.loc[missing_disc_idx, "Discount Percent"] = np.nan                    # Replace those Discount values with NaN

# Artificially duplicate 3 random rows to simulate duplicate records
dup_indices = np.random.choice(df.index, size=3, replace=False)          # Pick 3 random row indices
df = pd.concat([df, df.loc[dup_indices]], ignore_index=True)             # Append those rows again at the bottom

# ── 7. DATA CLEANING ────────────────────────────────────────

# Step 7a: Remove duplicate rows (keeps the first occurrence, drops the rest)
df.drop_duplicates(inplace=True)                                          # Remove the 3 duplicate rows we injected above
df.reset_index(drop=True, inplace=True)                                   # Reset the row index after dropping rows

# Step 7b: Fix the Date column data type — convert it from object/string to proper datetime
df["Date"] = pd.to_datetime(df["Date"])                                   # Convert the Date column to datetime64 type

# Step 7c: Handle missing values in 'Unit Price'
# Fill missing prices with the MEDIAN price of the same Product Category
df["Unit Price"] = df.groupby("Product Category")["Unit Price"].transform(
    lambda x: x.fillna(x.median())                                        # Within each category, fill NaN with that category's median price
)

# Step 7d: Handle missing values in 'Discount Percent'
# Fill missing discounts with 0.0 — a safe assumption (no discount applied)
df["Discount Percent"] = df["Discount Percent"].fillna(0.0)               # Replace any remaining NaN discounts with 0.0

# Step 7e: Fix integer column types (they may have become float after NaN injection)
df["Units Sold"] = df["Units Sold"].astype(int)                           # Ensure Units Sold is stored as integer

# Step 7f: Fix string/object column types for categoricals (good practice)
for col in ["Region", "Product Category", "Product Name", "Customer Segment"]:  # Loop over categorical columns
    df[col] = df[col].astype("category")                                          # Convert each to Pandas 'category' dtype (saves memory)

# ── 8. ADD THE CALCULATED 'TOTAL REVENUE' COLUMN ────────────
# Formula: Total Revenue = Units Sold × Unit Price × (1 - Discount Percent / 100)
df["Total Revenue"] = (
    df["Units Sold"]                          # Multiply number of units sold
    * df["Unit Price"]                        # ...by the price per unit
    * (1 - df["Discount Percent"] / 100)      # ...and apply the discount factor (e.g., 10% discount → multiply by 0.90)
)
df["Total Revenue"] = df["Total Revenue"].round(2)   # Round Total Revenue to 2 decimal places for currency formatting

# ── 9. PRINT RESULTS ────────────────────────────────────────

print("=" * 60)
print("FIRST 5 ROWS OF THE CLEANED DATASET")
print("=" * 60)
print(df.head())                              # Display the first 5 rows of the final DataFrame

print("\n" + "=" * 60)
print("SHAPE OF THE DATASET (rows, columns)")
print("=" * 60)
print(df.shape)                               # Print a tuple showing (number of rows, number of columns)

print("\n" + "=" * 60)
print("BASIC STATISTICAL SUMMARY (df.describe())")
print("=" * 60)
print(df.describe(include="all"))             # Print summary stats for ALL columns (numeric + categorical)

print("\n" + "=" * 60)
print("DATA TYPES OF EACH COLUMN")
print("=" * 60)
print(df.dtypes)                              # Show the data type of every column (good for verification)

print("\n" + "=" * 60)
print("MISSING VALUES AFTER CLEANING")
print("=" * 60)
print(df.isnull().sum())                      # Count any remaining NaN values per column (should all be 0)

# ── 10. SAVE THE CLEANED DATASET TO CSV ─────────────────────
df.to_csv("ecommerce_sales_data.csv", index=False)   # Save the final DataFrame to a CSV file without the row index
print("\n✅ Dataset saved to 'ecommerce_sales_data.csv' successfully!")    # Confirm the file was saved

# ============================================================
# ── 11. SQLITE DATABASE ANALYSIS ────────────────────────────
# ============================================================

import sqlite3    # Import Python's built-in SQLite library (no installation needed)

# ── Connect to (or create) a SQLite database file called shopmart.db ──
conn = sqlite3.connect("shopmart.db")    # If 'shopmart.db' doesn't exist yet, SQLite creates it automatically
cursor = conn.cursor()                   # Create a cursor object — this is how we send SQL commands to the database

# ── Load the cleaned Pandas DataFrame into the SQLite database ──
# Pandas' to_sql() writes every row of df into a table called 'sales' inside shopmart.db
# if_exists='replace' means: if the 'sales' table already exists, drop it and rebuild it fresh
# index=False means: don't write the Pandas row-index as a column in SQL
df.to_sql("sales", conn, if_exists="replace", index=False)
print("\n✅ DataFrame successfully loaded into 'shopmart.db' → table: 'sales'")

print("\n" + "=" * 60)
print("SQL BUSINESS QUERIES ON shopmart.db")
print("=" * 60)

# ──────────────────────────────────────────────────────────────
# QUERY 1: Top 5 Product Categories by Total Revenue
# Business Question: Which product categories are generating
# the most money? Helps decide where to invest in inventory.
# ──────────────────────────────────────────────────────────────
query1 = """
    SELECT "Product Category",                  -- Select the product category name
           ROUND(SUM("Total Revenue"), 2) AS total_revenue   -- Sum up all revenue per category, rounded to 2 decimals
    FROM sales                                  -- From our sales table
    GROUP BY "Product Category"                 -- Group rows that share the same category
    ORDER BY total_revenue DESC                 -- Sort from highest revenue to lowest
    LIMIT 5;                                    -- Only show the top 5 categories
"""
result1 = pd.read_sql_query(query1, conn)       # Run the query and load results into a Pandas DataFrame
print("\n📦 TOP 5 PRODUCT CATEGORIES BY TOTAL REVENUE:")
print(result1.to_string(index=False))           # Print the result neatly without the row index

# ──────────────────────────────────────────────────────────────
# QUERY 2: Monthly Revenue Trend across 2023
# Business Question: How did total sales revenue change month
# by month? Reveals seasonality and peak sales periods.
# ──────────────────────────────────────────────────────────────
query2 = """
    SELECT STRFTIME('%m', "Date") AS month,             -- Extract the 2-digit month number from the Date column
           STRFTIME('%Y-%m', "Date") AS year_month,     -- Extract full Year-Month label (e.g. '2023-04') for display
           ROUND(SUM("Total Revenue"), 2) AS monthly_revenue   -- Total revenue earned in that month
    FROM sales                                          -- From the sales table
    GROUP BY year_month                                 -- Group by each unique Year-Month combination
    ORDER BY month;                                     -- Sort chronologically Jan → Dec
"""
result2 = pd.read_sql_query(query2, conn)       # Execute query and fetch results as a DataFrame
print("\n📅 MONTHLY REVENUE TREND (2023):")
print(result2[["year_month", "monthly_revenue"]].to_string(index=False))  # Print only the readable columns

# ──────────────────────────────────────────────────────────────
# QUERY 3: Region-wise Average Discount Given
# Business Question: Are some regions offering higher discounts
# than others? Too much discounting hurts profit margins.
# ──────────────────────────────────────────────────────────────
query3 = """
    SELECT "Region",                                      -- Select the region name
           ROUND(AVG("Discount Percent"), 2) AS avg_discount   -- Calculate the average discount % per region
    FROM sales                                            -- From the sales table
    GROUP BY "Region"                                     -- Group rows by region
    ORDER BY avg_discount DESC;                           -- Show highest-discounting region first
"""
result3 = pd.read_sql_query(query3, conn)       # Run the query and capture results
print("\n🗺️  REGION-WISE AVERAGE DISCOUNT (%):")
print(result3.to_string(index=False))           # Print the table without row index

# ──────────────────────────────────────────────────────────────
# QUERY 4: Customer Segment Breakdown by Number of Orders
# Business Question: How many orders came from New, Returning,
# and VIP customers? Guides loyalty and retention strategy.
# ──────────────────────────────────────────────────────────────
query4 = """
    SELECT "Customer Segment",              -- Select the customer segment label
           COUNT(*) AS number_of_orders     -- Count total rows (orders) in each segment
    FROM sales                              -- From the sales table
    GROUP BY "Customer Segment"             -- Group by each unique customer segment
    ORDER BY number_of_orders DESC;         -- Show the most active segment first
"""
result4 = pd.read_sql_query(query4, conn)       # Execute and load into DataFrame
print("\n👥 CUSTOMER SEGMENT BREAKDOWN (by Orders):")
print(result4.to_string(index=False))           # Print without row index

# ──────────────────────────────────────────────────────────────
# QUERY 5: Top 3 Months with Highest Units Sold
# Business Question: Which months had the biggest sales volume?
# Useful for planning stock levels and supply chain logistics.
# ──────────────────────────────────────────────────────────────
query5 = """
    SELECT STRFTIME('%Y-%m', "Date") AS year_month,   -- Extract the Year-Month label from Date
           SUM("Units Sold") AS total_units            -- Sum all units sold within that month
    FROM sales                                         -- From the sales table
    GROUP BY year_month                                -- Group by month
    ORDER BY total_units DESC                          -- Sort from highest units sold to lowest
    LIMIT 3;                                           -- Only return the top 3 months
"""
result5 = pd.read_sql_query(query5, conn)       # Run the query and fetch results
print("\n🏆 TOP 3 MONTHS WITH HIGHEST UNITS SOLD:")
print(result5.to_string(index=False))           # Print the clean result table

# ── Close the database connection when all queries are done ──
conn.close()    # Always close the connection to free up system resources and avoid file lock issues
print("\n✅ All SQL queries complete. Database connection closed.")
print("📁 SQLite database saved as 'shopmart.db'")

# ============================================================
# ── 12. DATA VISUALIZATIONS ──────────────────────────────────
# ============================================================

import matplotlib.pyplot as plt    # Import Matplotlib for creating and saving charts
import matplotlib.ticker as mticker # Import ticker to format axis labels (e.g. currency, commas)
import seaborn as sns               # Import Seaborn for beautiful statistical charts built on top of Matplotlib

# Use a clean, professional Seaborn theme for all charts
sns.set_theme(style="whitegrid", font_scale=1.1)   # 'whitegrid' adds subtle grid lines; font_scale makes text bigger

print("\n" + "=" * 60)
print("GENERATING & SAVING CHARTS...")
print("=" * 60)

# ──────────────────────────────────────────────────────────────
# CHART 1: Bar Chart — Total Revenue by Product Category
# Business Question: Which category brings in the most revenue overall?
# ──────────────────────────────────────────────────────────────

# Group the DataFrame by 'Product Category', sum 'Total Revenue' for each, then sort descending
rev_by_cat = (
    df.groupby("Product Category", observed=True)["Total Revenue"]  # Group by category; observed=True avoids a Pandas warning for category dtype
    .sum()                                                            # Sum all revenue within each category
    .sort_values(ascending=False)                                     # Sort from highest to lowest revenue
    .reset_index()                                                    # Reset index so 'Product Category' becomes a normal column
)

fig, ax = plt.subplots(figsize=(9, 5))   # Create a figure and axes; figsize sets width x height in inches

# Draw the horizontal bar chart using the 'Blues_d' palette (dark to light blue shades)
sns.barplot(
    data=rev_by_cat,                         # Our aggregated DataFrame
    x="Total Revenue",                       # X-axis = Revenue values
    y="Product Category",                    # Y-axis = Category names
    palette="Blues_d",                       # Use dark-to-light blue color palette
    ax=ax,                                   # Draw on our specific axes object
    hue="Product Category",                  # Needed by Seaborn ≥0.12 to apply palette without deprecation warning
    legend=False                             # Don't show a legend (it's redundant here)
)

ax.set_title("Total Revenue by Product Category", fontsize=15, fontweight="bold", pad=12)  # Chart title
ax.set_xlabel("Total Revenue (USD)", fontsize=12)   # Label the X axis
ax.set_ylabel("Product Category", fontsize=12)      # Label the Y axis

# Format X-axis numbers with comma separators (e.g. 640000 → 640,000)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda val, _: f"${val:,.0f}"))

# Add the actual value labels at the end of each bar for easy reading
for bar in ax.patches:                                        # Loop over each bar in the chart
    width = bar.get_width()                                   # Get the width (= revenue value) of the bar
    ax.text(
        width + 2000,                                         # Place label slightly to the right of bar end
        bar.get_y() + bar.get_height() / 2,                  # Vertically center the label on the bar
        f"${width:,.0f}",                                     # Format as dollar amount with commas
        va="center", ha="left", fontsize=9, color="#333333"  # Vertical/horizontal alignment and style
    )

plt.tight_layout()                   # Automatically adjust padding so nothing gets cut off
plt.savefig("chart1.png", dpi=150)   # Save the chart as chart1.png at 150 DPI (good quality)
plt.close()                          # Close the figure to free memory (important in scripts)
print("✅ chart1.png saved — Bar Chart: Revenue by Category")


# ──────────────────────────────────────────────────────────────
# CHART 2: Line Chart — Monthly Revenue Trend across 2023
# Business Question: Are there seasonal peaks or slumps in sales?
# ──────────────────────────────────────────────────────────────

# Add a helper column 'Month' (period format, e.g. '2023-01') for grouping by month
df["Month"] = df["Date"].dt.to_period("M")             # Convert datetime to monthly period (Year-Month)

# Group by month, sum revenue, sort by month order
monthly_rev = (
    df.groupby("Month", observed=True)["Total Revenue"]  # Group by the new Month column
    .sum()                                                # Sum revenue for each month
    .reset_index()                                        # Bring Month back as a column
)
monthly_rev["Month"] = monthly_rev["Month"].astype(str)  # Convert Period to string for Matplotlib to plot on X axis

fig, ax = plt.subplots(figsize=(11, 5))   # Wider figure to fit 12 month labels comfortably

# Draw the line chart with markers at each data point
ax.plot(
    monthly_rev["Month"],          # X axis — month labels (e.g. '2023-01')
    monthly_rev["Total Revenue"],  # Y axis — total revenue per month
    color="#1565C0",               # A rich, dark blue line color
    linewidth=2.5,                 # Slightly thicker line for visibility
    marker="o",                    # Circle marker at each data point
    markersize=7,                  # Size of the circle markers
    markerfacecolor="#42A5F5",     # Fill the circles with a lighter blue
    markeredgecolor="#1565C0"      # Outline the circles with the darker blue
)

# Shade the area beneath the line for a modern look
ax.fill_between(
    monthly_rev["Month"],          # X range
    monthly_rev["Total Revenue"],  # Y range (top of fill)
    alpha=0.12,                    # Very light transparent fill (12% opacity)
    color="#1565C0"                # Same dark blue
)

ax.set_title("Monthly Revenue Trend — 2023", fontsize=15, fontweight="bold", pad=12)   # Chart title
ax.set_xlabel("Month", fontsize=12)             # X axis label
ax.set_ylabel("Total Revenue (USD)", fontsize=12)  # Y axis label
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda val, _: f"${val:,.0f}"))  # Format Y axis as dollars
plt.xticks(rotation=45, ha="right")            # Rotate month labels 45° so they don't overlap

plt.tight_layout()
plt.savefig("chart2.png", dpi=150)
plt.close()
print("✅ chart2.png saved — Line Chart: Monthly Revenue Trend")


# ──────────────────────────────────────────────────────────────
# CHART 3: Pie Chart — Orders by Customer Segment
# Business Question: What share of orders comes from New vs.
# Returning vs. VIP customers? Guides loyalty program decisions.
# ──────────────────────────────────────────────────────────────

# Count the number of orders per customer segment
segment_counts = df["Customer Segment"].value_counts()   # Returns a Series: {Returning: 110, VIP: 107, New: 83}

# Define custom colors for each slice — shades of blue
pie_colors = ["#1565C0", "#42A5F5", "#90CAF9"]          # Dark blue, medium blue, light blue

fig, ax = plt.subplots(figsize=(7, 7))   # Square figure works best for pie charts

wedges, texts, autotexts = ax.pie(
    segment_counts.values,               # The actual count values for each slice
    labels=segment_counts.index,         # Segment names as slice labels
    autopct="%1.1f%%",                   # Show percentage inside each slice with 1 decimal
    colors=pie_colors,                   # Our custom blue palette
    startangle=140,                      # Rotate so the largest slice starts at a nice angle
    pctdistance=0.82,                    # Place % labels 82% of the way to the edge (inside slice)
    wedgeprops={"edgecolor": "white", "linewidth": 2}  # White border between slices for clarity
)

for text in autotexts:                   # Style the percentage labels inside slices
    text.set_fontsize(12)
    text.set_color("white")              # White text shows up well on dark blue slices
    text.set_fontweight("bold")

ax.set_title("Orders by Customer Segment", fontsize=15, fontweight="bold", pad=16)  # Chart title

plt.tight_layout()
plt.savefig("chart3.png", dpi=150)
plt.close()
print("✅ chart3.png saved — Pie Chart: Orders by Customer Segment")


# ──────────────────────────────────────────────────────────────
# CHART 4: Boxplot — Unit Price Distribution by Category
# Business Question: What is the typical price range in each
# category? Are there outliers (very cheap or very expensive)?
# ──────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 6))   # Create figure for the boxplot

sns.boxplot(
    data=df,                              # Use the full cleaned DataFrame
    x="Product Category",                 # X axis — one box per product category
    y="Unit Price",                       # Y axis — distribution of unit prices within each category
    palette="Blues",                      # Use the 'Blues' palette (light shades per box)
    hue="Product Category",              # Assign hue for palette (Seaborn ≥0.12 requirement)
    legend=False,                         # No legend needed
    width=0.5,                            # Slightly narrower boxes for a clean look
    flierprops={"marker": "o",           # Style outlier dots as circles
                "markerfacecolor": "#1565C0",
                "markersize": 5,
                "alpha": 0.6},
    ax=ax                                 # Draw on our specific axes
)

ax.set_title("Unit Price Distribution by Product Category", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Product Category", fontsize=12)
ax.set_ylabel("Unit Price (USD)", fontsize=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda val, _: f"${val:,.0f}"))  # Dollar format Y axis

plt.tight_layout()
plt.savefig("chart4.png", dpi=150)
plt.close()
print("✅ chart4.png saved — Boxplot: Unit Price by Category")


# ──────────────────────────────────────────────────────────────
# CHART 5: Heatmap — Correlation between numeric columns
# Business Question: Do higher unit prices drive more revenue?
# Does discount reduce units sold? Reveals relationships between KPIs.
# ──────────────────────────────────────────────────────────────

# Select only the four numeric columns we want to correlate
numeric_cols = df[["Units Sold", "Unit Price", "Discount Percent", "Total Revenue"]]

# Compute the correlation matrix — values range from -1 (inverse) to +1 (direct relationship)
corr_matrix = numeric_cols.corr()   # Pearson correlation coefficient between every pair of columns

fig, ax = plt.subplots(figsize=(7, 6))   # Square-ish figure looks clean for a 4x4 heatmap

sns.heatmap(
    corr_matrix,                  # The 4×4 correlation matrix
    annot=True,                   # Show the actual correlation number inside each cell
    fmt=".2f",                    # Format numbers to 2 decimal places
    cmap="coolwarm",              # 'coolwarm': blue=negative correlation, red=positive correlation
    vmin=-1, vmax=1,              # Fix color scale from -1 to +1 so the colors are meaningful
    linewidths=0.5,               # Thin white lines between cells for readability
    linecolor="white",            # Cell border color
    square=True,                  # Force each cell to be a perfect square
    ax=ax
)

ax.set_title("Correlation Heatmap — Key Sales Metrics", fontsize=15, fontweight="bold", pad=14)
plt.xticks(rotation=30, ha="right", fontsize=10)   # Rotate X axis labels slightly
plt.yticks(rotation=0, fontsize=10)                # Keep Y axis labels horizontal

plt.tight_layout()
plt.savefig("chart5.png", dpi=150)
plt.close()
print("✅ chart5.png saved — Heatmap: Metric Correlations")


# ──────────────────────────────────────────────────────────────
# CHART 6: Countplot — Number of Orders by Region
# Business Question: Which regions are placing the most orders?
# Helps allocate sales teams and logistics budgets.
# ──────────────────────────────────────────────────────────────

# Count orders per region and sort from highest to lowest so bars are in a meaningful order
region_order = (
    df["Region"].value_counts()   # Count how many orders per region
    .index.tolist()               # Extract the region names sorted by count (most → least)
)

fig, ax = plt.subplots(figsize=(8, 5))   # Standard figure size

sns.countplot(
    data=df,                      # Full DataFrame
    x="Region",                   # X axis — one bar per region
    order=region_order,           # Sort bars from most to fewest orders
    palette="Blues_d",            # Dark-to-light blue palette
    hue="Region",                 # Needed by Seaborn ≥0.12 for palette
    legend=False,                 # No legend
    ax=ax
)

ax.set_title("Number of Orders by Region", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Region", fontsize=12)
ax.set_ylabel("Number of Orders", fontsize=12)

# Add the exact count on top of each bar
for bar in ax.patches:                             # Iterate through each bar
    count = int(bar.get_height())                  # Get bar height = number of orders
    ax.text(
        bar.get_x() + bar.get_width() / 2,         # Horizontally center the label on the bar
        bar.get_height() + 0.8,                    # Place just above the top of the bar
        str(count),                                # Display the count as a plain integer
        ha="center", va="bottom", fontsize=11, fontweight="bold", color="#1565C0"
    )

plt.tight_layout()
plt.savefig("chart6.png", dpi=150)
plt.close()
print("✅ chart6.png saved — Countplot: Orders by Region")

# ── Remove the helper 'Month' column we added just for Chart 2 ──
df.drop(columns=["Month"], inplace=True)   # Drop the temporary Period column so the DataFrame stays clean

print("\n🎉 All 6 charts saved successfully!")
print("   chart1.png → Revenue by Category (Bar)")
print("   chart2.png → Monthly Revenue Trend (Line)")
print("   chart3.png → Orders by Segment (Pie)")
print("   chart4.png → Unit Price Distribution (Boxplot)")
print("   chart5.png → Metric Correlations (Heatmap)")
print("   chart6.png → Orders by Region (Countplot)")
