from tracker import ExpenseTracker

def main():
    tracker = ExpenseTracker()

    tracker.add_expense("Lunch", 10, "Food")
    tracker.add_expense("Coffee", -5, "Food")  # Should be invalid
    tracker.add_expense("Taxi", 20, "Transport")

    print("\nAll Expenses:")
    for exp in tracker.expenses:
        print(exp)

    print("\nTotal खर्च:", tracker.get_total())

    print("\nFood Expenses:")
    food_expenses = tracker.filter_by_category("Food")
    for exp in food_expenses:
        print(exp)

if __name__ == "__main__":
    main()