# Task Tracker CLI

A simple command-line task tracker written in Python. Tasks are stored locally in `Tasks/tasks.json` and managed through a text-based menu.

## Project URL

https://roadmap.sh/projects/task-tracker

## Features

- Add new tasks
- View all tasks
- Update task status
- Delete completed tasks
- Persist task data in JSON format

## Requirements

- Python 3.10 or newer

## Project Structure

```text
Task-Tracker-CLI/
  main.py
  Tasks/
    tasks.json
```

## How to Run

From the `Task-Tracker-CLI` folder, run:

```bash
python main.py
```

If you are using a virtual environment, activate it first and then run the same command.

## Menu Options

When the program starts, you will see these options:

1. Add Task
2. Show Tasks
3. Update Task
4. Delete Done Tasks
5. Exit

## Task Data

Each task contains:

- `id`
- `description`
- `status`
- `createdAt`
- `updatedAt`

Task status values are:

- `Todo`
- `In Progress`
- `Done`

## Notes

- The app automatically creates `Tasks/tasks.json` if it does not exist.
- Deleted tasks are removed when their status is `Done`.
