import os
import json
from datetime import datetime

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

    year = datetime.now().year
    month = datetime.now().strftime("%B")

    print(f"Month: {month}")

    total_spent = 0
    for expense in expenses:
        if expense["year"] == year and expense["month"] == month:
            total_spent += int(expense["amount"])
    
    print(f"Spent: {total_spent}")

    with open("budget.txt", "r") as file:
        budget = file.read()

    print(f"Budget: {budget}")

    remaining = int(budget) - total_spent
    print(f"Remaining this month: {remaining}")




def view_breakdown(expenses):
    ...






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

def main():
    if not os.path.exists("budget.txt") or os.path.getsize("budget.txt") == 0:
        with open("budget.txt", "w") as file:
            file.write("500")

    # set default budget on first program run

    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            expenses = json.load(file)

    # store all expenses as a list of dicts to access them in code
    # the loaded variable is constantly up to date

    else:
        expenses = []

    # create empty list of expenses on first program run

    while True:
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
            print(expenses)
            exit()

if __name__ == "__main__":
    main()