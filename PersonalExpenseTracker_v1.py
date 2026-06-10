import os
import json
from datetime import datetime

def current_total_spent(expenses):
    year = datetime.now().year
    month = datetime.now().strftime("%B")

    # total_spent = 0
    # for expense in expenses:
    #     if expense["year"] == year and expense["month"] == month:
    #         total_spent += float(expense["amount"])

    total_spent = sum(
        float(expense["amount"]) for expense in expenses if expense["year"] == year and expense["month"] == month
        )

    return total_spent

def log_expense(expenses):
    year = datetime.now().year
    month = datetime.now().strftime("%B")

    amount = input("Amount: ")
    category = input("Category: ")
    description = input("Desc (\"no\" for none): ")

    new_expense = {"year": year, "month": month, "category": category, "amount": amount}
    
    if description != "no":
        new_expense["description"] = description

    # create new expense with year, month, category, amount, desc

    expenses.append(new_expense)

    with open("data.json", "w") as file:
        json.dump(expenses, file)

    # log/store new expense

def view_summary(expenses):
    # view summary of the current calendar month

    month = datetime.now().strftime("%B")

    print(f"Month: {month}")

    total_spent = current_total_spent(expenses)
    
    print(f"Spent: {total_spent}")

    with open("budget.txt", "r") as file:
        budget = file.read()

    print(f"Budget: {budget}")

    remaining = float(budget) - total_spent
    print(f"Remaining this month: {remaining}")

def view_breakdown(expenses):
    year = datetime.now().year
    month = datetime.now().strftime("%B")

    category_totals = {}
    for expense in expenses:
        if expense["year"] == year and expense["month"] == month:
            cat = expense["category"]
            category_totals[cat] = category_totals.get(cat, 0) + float(expense["amount"])

# use .get() so program does not crash when adding expense with no prior expense in category

    max_val = max(category_totals.values())

# determine most prominent category's amount for formatting chart

    # max_label = 0

    # for expense in expenses:
    #     if len(expense["category"]) > max_label:
    #         max_label = len(expense["category"])

    max_label = max(len(expense["category"]) for expense in expenses)

# determine char length of longest category for formatting chart

    print()

    title = f"{month} {year} Breakdown"
    print(f"\n{title}")

    print(f"{'\u2500' * len(title)}")

    for category, amount in category_totals.items():
        bar_length = int(amount / max_val * 40)   # each length based on max amount
        bar = '\u2588' * bar_length
        print(f"{category:>{max_label}} | {bar} {amount}")    # right aligned based
        print()

# display the bar chart

def remove_expense(expenses):
    ...







def set_monthly_budget():
    new_budget = input("Monthly Budget: ")

    with open("budget.txt", "w") as file:
        file.write(new_budget)

    # set new budget

def menu():
    print("Log Expense (1)\nView Summary (2)\nView Breakdown (3)\nSet Budget (4)")
    action = input("Action: ")
    
    return action

def default_budget():
    if not os.path.exists("budget.txt") or os.path.getsize("budget.txt") == 0:
        with open("budget.txt", "w") as file:
            file.write("500")

    # set default budget if budget does not exist

def main():
    default_budget()

    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            expenses = json.load(file)

    # store all expenses as a list of dicts to access them in code
    # the list can be modified in place in other functions if it is passed as a parameter)

    else:
        expenses = []

    # create empty list of expenses if expenses does not exist

    while True:
        total_spent = current_total_spent(expenses)
        
        with open("budget.txt", "r") as file:
            budget = file.read()
        
        remaining = float(budget) - total_spent

        if remaining <= float(budget) * 0.2:
            print(f"Be careful. Budget remaining: {remaining}")

    # remind user when nearing budget limit on every menu start

        action = menu()

        if action == "1":
            log_expense(expenses)
        
        elif action == "2":
            view_summary(expenses)

        elif action == "3":
            view_breakdown(expenses)

        elif action == "4":
            set_monthly_budget()
    
        else:
            exit()

if __name__ == "__main__":
    main()

# manage errors, do not allow non number amounts, etc