"""
Simple Command-Line Calculator
Run with: python calculator.py
Supports +, -, *, / on two numbers, then asks if you want to go again.
"""


def get_number(prompt):
    """Keep asking until the user enters a valid number (int or decimal)."""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("That's not a valid number, try again.")


def calculate(num1, num2, operation):
    """Perform the arithmetic and return the result (or None if invalid)."""
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            print("Error: can't divide by zero.")
            return None
        return num1 / num2
    else:
        print("Invalid operation.")
        return None


def main():
    print("===== SIMPLE CALCULATOR =====")

    while True:
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")

        print("Choose an operation: + - * /")
        operation = input("Operation: ").strip()

        result = calculate(num1, num2, operation)

        if result is not None:
            # Formats cleanly whether the result is a whole number or has decimals
            print(f"Result: {num1} {operation} {num2} = {result}")

        again = input("Calculate again? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
