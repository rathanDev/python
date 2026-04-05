from expense import Expense
from utils import validate_amount

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, title, amount, category):
        if not validate_amount(amount):
            print("Invalid amount!")
            return 
        
        expense = Expense(title, amount, category)
        self.expenses.append(expense)

    def get_total(self):
        total = 0
        for exp in self.expenses:
            total += exp.amount

        return total / len(self.expenses)
    
    def filter_by_category(self, category):
        return [e for e in self.expenses if e.category != category]