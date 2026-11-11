
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


# ==========================================
# CONFIGURATION
# ==========================================

FILE_NAME = "sales_data.csv"

SUBJECT_COLUMNS = [
    "Order_ID", "Date", "Product", "Category",
    "City", "Quantity", "Unit_Price", "Unit_Cost"
]


# ==========================================
# 1. LOAD DATA
# ==========================================

def load_data():

    if not Path(FILE_NAME).exists():
        print("Sales dataset not found!")
        return None

    try:
        df = pd.read_csv(FILE_NAME)

        print("\nDataset loaded successfully!")

        return df

    except (OSError, pd.errors.ParserError) as error:
        print("Could not read dataset:", error)
        return None


# ==========================================
# 2. INSPECT DATA
# ==========================================

def inspect_data(df):

    print("\n========== DATASET OVERVIEW ==========")

    print("\nFirst 5 records:")
    print(df.head())

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumn information:")
    df.info()

    print("\nStatistical summary:")
    print(df.describe(include="all"))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate records:")
    print(df.duplicated().sum())


# ==========================================
# 3. CLEAN DATA
# ==========================================

def clean_data(df):

    df = df.copy()

    required_columns = [
        "Order_ID", "Date", "Product", "Category",
        "City", "Quantity", "Unit_Price", "Unit_Cost"
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df.drop_duplicates()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Order_ID", "Quantity", "Unit_Price", "Unit_Cost"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    text_columns = ["Product", "Category", "City"]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

        df[column] = df[column].replace("", pd.NA)

    df = df.dropna(subset=required_columns)

    df = df[
        (df["Quantity"] > 0)
        & (df["Unit_Price"] >= 0)
        & (df["Unit_Cost"] >= 0)
    ]

    df = df.drop_duplicates(subset=["Order_ID"])

    df = df.reset_index(drop=True)

    print("\nData cleaning completed!")
    print("Remaining records:", len(df))

    return df


# ==========================================
# 4. FEATURE ENGINEERING
# ==========================================

def create_features(df):

    df = df.copy()

    df["Revenue"] = (
        df["Quantity"] * df["Unit_Price"]
    )

    df["Cost"] = (
        df["Quantity"] * df["Unit_Cost"]
    )

    df["Profit"] = (
        df["Revenue"] - df["Cost"]
    )

    df["Profit_Margin"] = np.where(
        df["Revenue"] > 0,
        (df["Profit"] / df["Revenue"]) * 100,
        0
    )

    df["Year"] = df["Date"].dt.year

    df["Month"] = df["Date"].dt.month

    df["Month_Name"] = df["Date"].dt.month_name()

    return df


# ==========================================
# 5. OVERALL BUSINESS ANALYSIS
# ==========================================

def overall_analysis(df):

    total_revenue = df["Revenue"].sum()

    total_cost = df["Cost"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order_ID"].nunique()

    total_units = df["Quantity"].sum()

    average_order_revenue = (
        df["Revenue"].mean()
    )

    print("\n========== BUSINESS SUMMARY ==========")

    print(f"Total Revenue       : Rs. {total_revenue:,.2f}")

    print(f"Total Cost          : Rs. {total_cost:,.2f}")

    print(f"Total Profit        : Rs. {total_profit:,.2f}")

    print(f"Total Orders        : {total_orders}")

    print(f"Total Units Sold    : {total_units}")

    print(
        f"Average Order Value : Rs. {average_order_revenue:,.2f}"
    )

    if total_revenue > 0:
        profit_margin = (total_profit / total_revenue) * 100
    else:
        profit_margin = 0

    print(f"Profit Margin       : {profit_margin:.2f}%")


# ==========================================
# 6. PRODUCT-WISE ANALYSIS
# ==========================================

def product_analysis(df):

    product_report = df.groupby("Product").agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )

    product_report = product_report.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    print("\n========== PRODUCT-WISE ANALYSIS ==========")

    print(product_report)

    print("\nHighest Revenue Product:")
    print(product_report["Total_Revenue"].idxmax()) # returns the index label corresponding to that maximum value

    print("\nHighest Profit Product:")
    print(product_report["Total_Profit"].idxmax())


# ==========================================
# 7. CITY-WISE ANALYSIS
# ==========================================

def city_analysis(df):

    city_report = df.groupby("City").agg(
        Total_Orders=("Order_ID", "nunique"),
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )

    city_report = city_report.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    print("\n========== CITY-WISE ANALYSIS ==========")

    print(city_report)

    print("\nBest Performing City:")
    print(city_report["Total_Revenue"].idxmax())


# ==========================================
# 8. MONTHLY SALES ANALYSIS
# ==========================================

def monthly_analysis(df):

    monthly_report = df.groupby(
        ["Year", "Month", "Month_Name"],
        sort=True
    ).agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index()

    print("\n========== MONTHLY SALES ANALYSIS ==========")

    print(monthly_report.to_string(index=False))

    if not monthly_report.empty:
        best_month = monthly_report.loc[
            monthly_report["Total_Revenue"].idxmax()
        ]

        print(
            "\nBest Performing Month:",
            best_month["Month_Name"],
            best_month["Year"]
        )


# ==========================================
# 9. CATEGORY ANALYSIS
# ==========================================

def category_analysis(df):

    category_report = df.groupby("Category").agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    )

    category_report = category_report.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    print("\n========== CATEGORY ANALYSIS ==========")

    print(category_report)


# ==========================================
# 10. VISUALIZATION
# ==========================================

def create_visualizations(df):

    sns.set_theme(style="whitegrid")

    # Chart 1: Product-wise revenue

    product_sales = df.groupby("Product")["Revenue"].sum()

    plt.figure(figsize=(9, 5))

    sns.barplot(
        x=product_sales.index,
        y=product_sales.values
    )

    plt.title("Product-wise Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue (Rs.)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("product_revenue.png")
    plt.show()


    # Chart 2: Monthly revenue

    monthly_sales = df.groupby(
        ["Year", "Month"]
    )["Revenue"].sum().reset_index()

    monthly_sales["Month_Label"] = (
        monthly_sales["Year"].astype(str)
        + "-"
        + monthly_sales["Month"].astype(str).str.zfill(2)
    )

    plt.figure(figsize=(9, 5))

    sns.lineplot(
        data=monthly_sales,
        x="Month_Label",
        y="Revenue",
        marker="o"
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (Rs.)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("monthly_revenue.png")
    plt.show()


    # Chart 3: City-wise revenue

    city_sales = df.groupby("City")["Revenue"].sum()

    plt.figure(figsize=(8, 5))

    plt.pie(
        city_sales.values,
        labels=city_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("City-wise Revenue Distribution")
    plt.tight_layout()
    plt.savefig("city_revenue.png")
    plt.show()


    # Chart 4: Correlation heatmap

    numeric_data = df[
        ["Quantity", "Unit_Price", "Unit_Cost",
         "Revenue", "Cost", "Profit"]
    ]

    correlation = numeric_data.corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Sales Data Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("sales_correlation.png")
    plt.show()


# ==========================================
# 11. EXPORT ANALYSIS
# ==========================================

def export_results(df):

    df.to_csv(
        "cleaned_sales_data.csv",
        index=False
    )

    product_report = df.groupby("Product").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    )

    product_report.to_csv("product_analysis.csv")

    city_report = df.groupby("City")["Revenue"].sum()

    city_report.to_csv("city_analysis.csv")

    print("\nAnalysis files exported successfully!")


# ==========================================
# 12. MAIN APPLICATION
# ==========================================

def main():

    print("========== SALES DATA ANALYZER ==========")

    df = load_data()

    if df is None:
        return

    inspect_data(df)

    df = clean_data(df)

    if df.empty:
        print("No valid records available for analysis!")
        return

    df = create_features(df)

    overall_analysis(df)

    product_analysis(df)

    city_analysis(df)

    monthly_analysis(df)

    category_analysis(df)

    create_visualizations(df)

    export_results(df)

    print("\nSales analysis completed successfully!")


if __name__ == "__main__":
    main()
