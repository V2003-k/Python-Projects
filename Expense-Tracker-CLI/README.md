# Expense Tracker CLI

A simple Python command-line application to track personal expenses, save them locally, and view summaries by month or year.

## Features

- Add new expenses
- Update existing expenses
- Delete expenses by ID
- List all expenses in a table
- View total expense summary
- View monthly expense summary
- Saves data to JSON and CSV files

## Project Structure

```text
Expense-Tracker-CLI/
├── main.py
├── output/
│   └── output.json
└── Expense List/
    └── Expense-List.csv
```

## Requirements

- Python 3.8+
- `pandas`
- `tabulate`

## Installation

Install the required packages:

```powershell
pip install pandas tabulate
```

If you want to use a virtual environment on Windows:

```powershell
cd "Expense-Tracker-CLI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pandas tabulate
```

## Usage

Run the application:

```powershell
python main.py
```

You will see this prompt:

```text
expense-tracker
```

## Commands

### Add an expense

```text
add --description "Lunch" --amount 250
```

### List all expenses

```text
list
```

### Update an expense

```text
update --id 1 --description "Dinner" --amount 300
```

### View summary

```text
summary
```

### View monthly summary

```text
summary --month 4 --year 2026
```

### Delete an expense

```text
delete --id 1
```

### Exit the application

```text
quit
```

## Data Storage

- `output/output.json` stores expense data in JSON format
- `Expense List/Expense-List.csv` is generated for tabular viewing and summaries

## Notes

- Expense IDs are auto-generated.
- The `quit` command is case-sensitive.
- Monthly summary works only if valid `--month` and `--year` values are provided.
- Data files are created automatically if they do not exist.

## Example

```text
expense-tracker add --description "Books" --amount 500
Expense Added Successfully (ID:1)

expense-tracker list
ID  Date        Description  Amount
1   2026-04-22  Books        500
```

## Future Improvements

- Add better input validation
- Support categories for expenses
- Add filtering by date range
- Add unit tests
- Improve command parsing and error messages