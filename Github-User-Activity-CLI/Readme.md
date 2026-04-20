# GitHub User Activity CLI

A simple Python CLI tool that fetches a GitHub user's recent public activity and prints it in a human-readable format.

## Features

- Fetches recent public events from the GitHub API
- Saves raw API response to `output/output.json`
- Displays formatted activity in terminal, including:
  - Push events
  - Issues events
  - Watch (star) events
  - Pull request events
  - Fork events
  - Create/Delete events
  - Issue/PR comment events

## Project Structure

```text
Github-User-Activity-CLI/
├── main.py
└── output/
    └── output.json
```

## Requirements

- Python 3.8+
- `requests`

## Installation (Windows PowerShell)

```powershell
cd "v:\Python Projects\Python-Projects\Github-User-Activity-CLI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install requests
```

## Usage

```powershell
python main.py
```

Then enter a GitHub username at the prompt:

```text
github-activity torvalds
```

To exit, type:

```text
github-activity Quit
```

> Note: Exit command is case-sensitive (`Quit`).

## Example Output

```text
Output:
 - Pushed 3 to torvalds/linux
 - Opened a pull request in some/repo
 - Starred another/repo
```

## Error Handling

The script handles:

- HTTP errors
- Connection errors
- Timeout errors
- Generic request exceptions
- 404 (user not found)

## Notes

- GitHub API rate limits unauthenticated requests.
- Only public events are available.
- `output/output.json` is overwritten on each successful request.

## Possible Improvements

- Add GitHub token support
- Add command-line arguments (e.g., `python main.py <username>`)
- Improve event coverage and formatting
- Add retries/logging
- Add unit tests