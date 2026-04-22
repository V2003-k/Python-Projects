import os
import json
import shlex
import pandas as pd
from pathlib import Path
from datetime import date
from tabulate import tabulate

# Create output directories if they do not exist
OP_DIR_PATH = Path("output")
OP_DIR_PATH.mkdir(exist_ok=True, parents=True)

DIR_PATH = Path("Expense List")
DIR_PATH.mkdir(exist_ok=True, parents=True)

# File paths
OP_PATH = OP_DIR_PATH / "output.json"
PATH = DIR_PATH / "Expense-List.csv"

# Initialize JSON file with empty list on first run
if not os.path.exists(OP_PATH):
    with open(OP_PATH, "w") as file:
        json.dump([], file, indent=4)

# Load exiting expense data from JSON
try:
    with open(OP_PATH, "r") as file:
        DATA = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print("Error reading data file. Resetting data...")
    DATA = []

def ele_id():
    """ Return the next available expense id """
    if not DATA:
        return 1
    return max(ele["ID"] for ele in DATA) + 1

# Expense model for a single entry
class Expense:
    id: int
    date: date
    description: str
    amount: float

    def __init__(self, description: str, amount: float):
        self.id = ele_id()
        self.date = date.today().isoformat()
        self.description = description
        self.amount = amount

    def to_dict(self):
        """ Convert Expense object to dictionary format for JSON storage """
        return {
            "ID": self.id,
            "Date": self.date,
            "Description": self.description,
            "Amount": self.amount
        }

def add_expense(description: str, amount):
    """ Add a new expense after validating description and amount """
    # Validate description
    if not isinstance(description, str) or not description.strip():
        print("Invalid Description!")
        return
    # Validate and convert amount
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid Amount!")
        return
    # Create and append expense
    ele = Expense(description=description, amount=amount).to_dict()
    DATA.append(ele)
    # Persist data to JSON
    try: 
        with open(OP_PATH, "w") as file:
            json.dump(DATA, file, indent=4)
    except OSError as err:
        print(f"File Writing Failed: {err}")
    except TypeError as err:
        print(f"Data could not be serialized to JSON: {err}")

def update_expense(id, **kwargs):
    """ Update an existing expense by id using optional description or amount """
    found = False
    for ele in DATA:
        if ele.get("ID") == id:
            found = True
            # Update description if provided
            if "description" in kwargs:
                ele["Description"] = kwargs["description"]
            # Update amount if provided
            if "amount" in kwargs:
                ele["Amount"] = float(kwargs["amount"])
            break

    if not found:
        print("Expense not found!")
    # Persist update data
    try:
        with open(OP_PATH, "w") as file:
            json.dump(DATA, file, indent=4)
    except OSError as err:
        print(f"File Writing Failed: {err}")
    except TypeError as err:
        print(f"Data could not be serialized to JSON: {err}")

def delete_expense(id):
    """ Delete an expense by id """
    global DATA
    id = int(id)
    # Keep all expenses except the one matchin the id
    DATA = [ele for ele in DATA if ele['ID'] != id]
    # Persist updated data
    try:
        with open(OP_PATH, "w") as file:
            json.dump(DATA, file, indent=4)
    except OSError as err:
        print(f"File Writing Failed: {err}")
    except TypeError as err:
        print(f"Data could not be serialized to JSON: {err}")

def load_to_csv():
    """ Export in memory expense data to CSV file """
    df = pd.DataFrame(DATA)
    df.to_csv(PATH, index=False)

def view_all_expense():
    """ Return all expenses formatted as a plain table string """
    load_to_csv()
    data = pd.read_csv(PATH)
    expense = tabulate(data, headers="keys", tablefmt="plain", showindex=False)
    return expense

def expense_summery():
    """ Return total sum of all expenses """
    data = pd.read_csv(PATH)
    total = data["Amount"].sum()
    return f"Total expenses: ₹{total}"

def get_expense_by_month(month, year):
    """ Return total expenses for a specific month and year """
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }
    data = pd.read_csv(PATH)
    month = int(month)
    year = int(year)
    total = 0
    # Sum amounts where expense date matches requested month and year
    for _, row in data.iterrows():
        try:
            exp_date = date.fromisoformat(row["Date"])
        except Exception:
            continue
        
        if exp_date.month == month and exp_date.year == year:
            total += row["Amount"]

    return f"Total expences for {months[month]}: ₹{total}"

if __name__ == "__main__":
    while True:
        user_input = input("expense-tracker ").strip()
        # Ignore empty command
        if not user_input:
            continue
        # Parse command safely
        args = shlex.split(user_input)

        command = args[0]

        if command == "add":
            description = None
            amount = None

            for i in range(len(args)):
                if args[i] == "--description":
                    description = args[i + 1]
                if args[i] == "--amount":
                    amount = args[i + 1]
            
            if description and amount:
                add_expense(description, amount)
                id = DATA[-1]["ID"]
                print(f"Expense Added Successfully (ID:{id})")
            else:
                print("Missing --description or --amount")
        elif command == "list":
            expenses = view_all_expense()
            print(expenses)
        elif command == "update":
            eid = None
            description = None
            amount = None

            for i in range(len(args)):
                if args[i] == "--id":
                    eid = args[i + 1]
                if args[i] == "--description":
                    description = args[i + 1]
                if args[i] == "--amount":
                    amount = args[i + 1]
            
            if eid:
                kwargs = {}
                if description:
                    kwargs["description"] = description
                if amount:
                    kwargs["amount"] = amount
                update_expense(eid, **kwargs)
                print("Expense Update Successfully!")
            else:
                print("Missing --eid")
        elif command == "summary":
            month = None
            year = None

            for i in range(len(args)):
                if args[i] == "--month":
                    month = args[i + 1]
                if args[i] == "--year":
                    year = args[i + 1]
            
            if month and year:
                monthly_summary = get_expense_by_month(month, year)
                print(monthly_summary)
            elif month or year:
                print("Both --month and --year required")
            else:
                summary = expense_summery()
                print(summary)
        elif command == "delete":
            id = None

            for i in range(len(args)):
                if args[i] == "--id":
                    id = args[i + 1]

            if id:
                delete_expense(id)
                print("Expense deleted successfully")
            else:
                print("Missing --id")
        elif command == "quit":
            break