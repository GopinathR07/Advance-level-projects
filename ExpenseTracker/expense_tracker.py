
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime

DB_NAME = "expenses.db"


# ==========================================
# 1. DATABASE CONNECTION AND TABLE CREATION
# ==========================================

def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    connection = get_connection() # Establishes the connection with the database
    cursor = connection.cursor() # Executes SQL statements

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL
                CHECK(transaction_type IN ('income', 'expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            description TEXT,
            transaction_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
    print("Database initialized successfully!")


# ==========================================
# 2. ADD A TRANSACTION
# ==========================================

def add_transaction():
    transaction_type = input(
        "Enter type (income/expense): "
    ).strip().lower()

    if transaction_type not in ("income", "expense"):
        print("Invalid transaction type!")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty!")
        return

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid number!")
        return

    description = input("Enter description: ").strip()

    transaction_date = input(
        f"Enter date (YYYY-MM-DD) [default: {date.today()}]: "
    ).strip()

    if not transaction_date:
        transaction_date = date.today().isoformat()

    try:
        datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date! Use YYYY-MM-DD.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (transaction_type, category, amount, description, transaction_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_type,
        category,
        amount,
        description,
        transaction_date
    ))

    connection.commit()
    connection.close()

    print("Transaction added successfully!")


# ==========================================
# 3. VIEW ALL TRANSACTIONS
# ==========================================

def view_transactions():
    connection = get_connection()

    query = """
        SELECT * FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    if df.empty:
        print("No transactions found!")
        return

    print("\n========== ALL TRANSACTIONS ==========")
    print(df.to_string(index=False))


# ==========================================
# 4. FINANCIAL SUMMARY
# ==========================================

def show_summary():
    connection = get_connection()

    query = """
        SELECT transaction_type, SUM(amount) AS total
        FROM transactions
        GROUP BY transaction_type
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    income = 0
    expenses = 0

    for _, row in df.iterrows():
        if row["transaction_type"] == "income":
            income = row["total"]
        elif row["transaction_type"] == "expense":
            expenses = row["total"]

    balance = income - expenses

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Income   : Rs. {income:.2f}")
    print(f"Total Expenses : Rs. {expenses:.2f}")
    print(f"Balance        : Rs. {balance:.2f}")


# ==========================================
# 5. CATEGORY-WISE EXPENSE REPORT
# ==========================================

def category_report():
    connection = get_connection()

    query = """
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    if df.empty:
        print("No expense records found!")
        return

    print("\n========== CATEGORY-WISE EXPENSES ==========")
    print(df.to_string(index=False))


# ==========================================
# 6. MONTHLY EXPENSE REPORT
# ==========================================

def monthly_report():
    connection = get_connection()

    query = """
        SELECT
            substr(transaction_date, 1, 7) AS month,
            SUM(amount) AS total_expenses
        FROM transactions
        WHERE transaction_type = 'expense'
        GROUP BY month
        ORDER BY month
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    if df.empty:
        print("No expense records found!")
        return

    print("\n========== MONTHLY EXPENSES ==========")
    print(df.to_string(index=False))


# ==========================================
# 7. UPDATE A TRANSACTION
# ==========================================

def update_transaction():
    try:
        transaction_id = int(input("Enter transaction ID: "))
        new_amount = float(input("Enter new amount: "))

        if new_amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Enter valid numeric values!")
        return

    new_category = input("Enter new category: ").strip()

    if not new_category:
        print("Category cannot be empty!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET amount = ?, category = ?
        WHERE id = ?
    """, (new_amount, new_category, transaction_id))

    updated_rows = cursor.rowcount
    connection.commit()
    connection.close()

    if updated_rows > 0:
        print("Transaction updated successfully!")
    else:
        print("Transaction ID not found!")


# ==========================================
# 8. DELETE A TRANSACTION
# ==========================================

def delete_transaction():
    try:
        transaction_id = int(input("Enter transaction ID: "))
    except ValueError:
        print("Enter a valid transaction ID!")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    deleted_rows = cursor.rowcount
    connection.commit()
    connection.close()

    if deleted_rows > 0:
        print("Transaction deleted successfully!")
    else:
        print("Transaction ID not found!")


# ==========================================
# 9. EXPORT TRANSACTIONS TO CSV
# ==========================================

def export_to_csv():
    connection = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY transaction_date",
        connection
    )

    connection.close()

    if df.empty:
        print("No data available to export!")
        return

    df.to_csv("expense_report.csv", index=False)
    print("Data exported to expense_report.csv!")


# ==========================================
# 10. CATEGORY EXPENSE CHART
# ==========================================

def show_expense_chart():
    connection = get_connection()

    query = """
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'expense'
        GROUP BY category
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    if df.empty:
        print("No expense records available for chart!")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(df["category"], df["total"])

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (Rs.)")
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig("expense_chart.png")
    plt.show()


# ==========================================
# 11. MAIN MENU
# ==========================================

def main():
    initialize_database()

    while True:
        print("\n========== PERSONAL EXPENSE TRACKER ==========")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Financial Summary")
        print("4. Category-wise Expenses")
        print("5. Monthly Expenses")
        print("6. Update Transaction")
        print("7. Delete Transaction")
        print("8. Export to CSV")
        print("9. Show Expense Chart")
        print("10. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            category_report()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            update_transaction()
        elif choice == "7":
            delete_transaction()
        elif choice == "8":
            export_to_csv()
        elif choice == "9":
            show_expense_chart()
        elif choice == "10":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice! Select 1-10.")


if __name__ == "__main__":
    main()
