import os

def log_expense():
    amount = input("Amount: ")
    category = input("Category: ")
    description = input("Desc (\"no\" for none): ")

    new_expense = {"category": category, "amount": amount}
    
    if description != "no":
        new_expense["description"] = description

    # logs new expense with category amount and description

    with open("data.txt", "a") as file:
        file.write(f"{new_expense}\n")

    # store the new expense as a dict in data file

def view_summary():
    ...

def view_breakdown():
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

    while True:
        action = menu()

        if action == "1":
            log_expense()
        
        elif action == "2":
            view_summary()

        elif action == "3":
            view_breakdown()

        elif action == "4":
            set_monthly_budget()
    
        else:
            exit()

if __name__ == "__main__":
    main()