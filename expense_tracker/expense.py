class Expense:
    def __init__(self, title, amount, category):
        self.title = title
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.category})"
    
