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

def set_budget():
    ...

def menu():
    print("Log Expense (1)\nView Summary (2)\nView Breakdown (3)\nSet Budget (4)")
    action = input("Action: ")
    
    return action

def main():
    while True:
        action = menu()

        if action == "1":
            log_expense()
        
        elif action == "2":
            view_summary()

        elif action == "3":
            view_breakdown()

        elif action == "4":
            set_budget()
    
        else:
            exit()

if __name__ == "__main__":
    main()