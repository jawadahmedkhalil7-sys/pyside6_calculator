#
# from database import create_table, save_calculation, get_calculations
#
#
# # Database table tayyar karna
# create_table()
#
#
# print("===== Welcome Calculator =====")
#
#
# while True:
#
#     # Pehla number
#     while True:
#         try:
#             number1 = float(input("Enter your first number: "))
#             break
#         except ValueError:
#             print("Please enter a valid number!")
#
#     # Operator
#     while True:
#         operator = input("Enter your operator (+ - * /): ")
#
#         if operator in ["+", "-", "*", "/"]:
#             break
#         else:
#             print("Invalid operator! Please enter + - * /.")
#
#     # Doosra number
#     while True:
#         try:
#             number2 = float(input("Enter your second number: "))
#             break
#         except ValueError:
#             print("Please enter a valid number!")
#
#     # Calculation
#     result = None
#
#     if operator == "+":
#         result = number1 + number2
#
#     elif operator == "-":
#         result = number1 - number2
#
#     elif operator == "*":
#         result = number1 * number2
#
#     elif operator == "/":
#         if number2 == 0:
#             print("Cannot divide by zero!")
#         else:
#             result = number1 / number2
#
#     # Result print aur database mein save
#     if result is not None:
#         print("Result:", result)
#
#         try:
#             save_calculation(number1, operator, number2, result)
#             print("Calculation saved to database!")
#
#         except Exception as error:
#             print("Database save error:", error)
#
#     # Purani calculations dekhna
#     while True:
#         history = input(
#             "Do you want to see calculation history? (yes/no): "
#         ).lower().strip()
#
#         if history in ["yes", "no"]:
#             break
#         else:
#             print("Please enter yes or no!")
#
#     if history == "yes":
#         records = get_calculations()
#
#         print("\n===== Calculation History =====")
#
#         if records:
#             for record in records:
#                 print(
#                     f"ID: {record[0]} | "
#                     f"{record[1]} {record[2]} {record[3]} = {record[4]} | "
#                     f"Date: {record[5]}"
#                 )
#         else:
#             print("No calculations found!")
#
#         print()
#
#     # Dobara calculation karna
#     while True:
#         again = input(
#             "Do you want to calculate again? (yes/no): "
#         ).lower().strip()
#
#         if again == "yes":
#             break
#
#         elif again == "no":
#             print("Calculator closed!")
#             exit()
#
#         else:
#             print("Please enter yes or no!")


import sqlite3
from pathlib import Path


# Database file hamesha isi folder mein rahegi
DATABASE_NAME = Path(__file__).resolve().parent / "calculator.db"


# Database connection
def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA busy_timeout = 5000")
    return connection


# Table banana aur purani table update karna
def create_table():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number1 REAL NOT NULL,
                operator TEXT NOT NULL,
                number2 REAL NOT NULL,
                result REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Existing table mein missing column check karna
        cursor.execute("PRAGMA table_info(calculations)")
        columns = [column[1] for column in cursor.fetchall()]

        if "created_at" not in columns:
            cursor.execute("""
                ALTER TABLE calculations
                ADD COLUMN created_at TIMESTAMP
            """)

            cursor.execute("""
                UPDATE calculations
                SET created_at = CURRENT_TIMESTAMP
                WHERE created_at IS NULL
            """)


# Calculation save karna

def save_calculation(number1, operator, number2, result):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO calculations
                (number1, operator, number2, result, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (number1, operator, number2, result))



# Saved calculations hasil karna
def get_calculations():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, number1, operator, number2, result, created_at
            FROM calculations
            ORDER BY id DESC
        """)

        return cursor.fetchall()


# Ek calculation delete karna
def delete_calculation(calculation_id):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM calculations WHERE id = ?",
            (calculation_id,)
        )

        return cursor.rowcount > 0


# Tamam history delete karna
def clear_calculations():
    with get_connection() as connection:
        connection.execute("DELETE FROM calculations")


# File import hone par bhi table ready hogi
create_table()


# Direct run karne par saved history show hogi
if __name__ == "__main__":
    print("Database ready!")
    print("\n===== Saved Calculations =====")

    for record in get_calculations():
        print(record)

