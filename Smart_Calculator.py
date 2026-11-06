
# Project 2: Smart Calculator


# Step 1: Define mathematical functions

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")

    return a / b


def power(a, b):
    return a ** b


def remainder(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot calculate remainder with zero.")

    return a % b


# Step 2: Map operations to functions

operations = {
    "1": add,
    "2": subtract,
    "3": multiply,
    "4": divide,
    "5": power,
    "6": remainder
}


# Step 3: Display the calculator menu

def display_menu():
    print("\n===== SMART CALCULATOR =====")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power")
    print("6. Remainder")
    print("7. Exit")


# Step 4: Main program

def main():

    while True:

        display_menu()

        choice = input("Choose an operation (1-7): ").strip()

        if choice == "7":
            print("Thank you for using Smart Calculator!")
            break

        if choice not in operations:
            print("Invalid choice. Please select 1-7.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            selected_function = operations[choice]

            result = selected_function(num1, num2)

            print(f"Result: {result}")

        except ValueError:
            print("Invalid input! Please enter numeric values.")

        except ZeroDivisionError as error:
            print(f"Math Error: {error}")


# Step 5: Execute the program

if __name__ == "__main__":
    main()
