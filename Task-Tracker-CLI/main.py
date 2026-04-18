import os
import json
from pathlib import Path
from enum import Enum
from datetime import datetime

# Create path for tasks directory
FILE_PATH = Path("Tasks")
FILE_PATH.mkdir(exist_ok=True, parents=True)

# Create path for tasks.json
PATH = FILE_PATH / "tasks.json"

# Creates tasks.json file
if not os.path.exists(PATH):
    with open(PATH, "w") as f:
        json.dump([], f, indent=4)

# Load tasks.json data to variable DATA
with open(PATH, "r") as f:
    DATA = json.load(f)

def task_id():
    if not DATA:
        return 1
    return max(task["id"] for task in DATA) + 1

class Status(Enum):
    todo = "Todo"
    in_progress = "In Progress"
    done = "Done"

class Task:
    id: int
    description: str
    status: Status
    createdAt: datetime
    updatedAt: datetime

    def __init__(self, description: str, status: Status):
        self.id = task_id()
        self.description = description
        self.status = status
        self.createdAt = datetime.now().isoformat()
        self.updatedAt = datetime.now().isoformat()

    def to_dict(self):
        """ This function convers object to dictionary """
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

# Add tasks
def add_task():
    """ Using this function you can add task to tasks.json """
    description = input("Enter Task Description: ")
    
    task = Task(description, Status.todo)
    DATA.append(task.to_dict())
    with open(PATH, "w") as f:
        json.dump(DATA, f, indent=4)

    print("Task Added Successfully!", end="\n")
    return

# Display all tasks
def display_all_tasks():
    """ This function helps to display all the tasks on screen """
    for data in DATA:
        print("-" * 30, end="\n")
        print(f"ID: {data["id"]}")
        print(f"DESCRIPTION: {data["description"]}")
        print(f"STATUS: {data["status"]}")
        print(f"CREATED AT: {data["createdAt"]}")
        print(f"UPDATED AT: {data["updatedAt"]}")
        print("-" * 30, end="\n")

# Update tasks using task id
def update_task_status():
    """ This function helps to update tasks mainly task status """
    id = int(input("Enter Task Id of Task to update: "))
    for data in DATA:
        if data["id"] == id:
            status = input("Update Task Status to (Todo / In Progress / Done): ")
            try:
                data["status"] = Status(status).value
                data["updatedAt"] = datetime.now().isoformat()

                with open(PATH, "w") as f:
                    json.dump(DATA, f, indent=4)

                print("Task Updated Successfully!", end="\n")
                return
            except ValueError:
                print("Wrong Value !", end="\n")
                return 
            
    print("Task not found", end="\n")
    
# Delete the task
def delete_task():
    """ This function helps to delete the task based on task status if status is done then it deletes that task """
    global DATA
    DATA = [task for task in DATA if task["status"] != "Done"]
    with open(PATH, "w") as f:
        json.dump(DATA, f, indent=4)

if __name__ == "__main__":
    while True:
        print("\n1. Add Task")
        print("2. Show Tasks")
        print("3. Update Task")
        print("4. Delete Done Tasks")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            display_all_tasks()
        elif choice == "3":
            update_task_status()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")