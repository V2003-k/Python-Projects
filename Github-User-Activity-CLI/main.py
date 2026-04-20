import os
import json
import requests
from pathlib import Path
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

FILE_PATH = Path("output")
FILE_PATH.mkdir(exist_ok=True, parents=True)

PATH = FILE_PATH / "output.json"

if not os.path.exists(PATH):
    with open(PATH, "w") as file:
        json.dump({}, file, indent=4)

def get_user_activity(username):
    try:
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            with open(PATH, "w") as file:
                json.dump(response.json(), file, indent=4)
        if response.status_code == 404:
            print(f"Error 404: requested user {username} not found")

    except HTTPError as http_err:
        print(f"An HTTP Error Occured: {http_err}")
    except ConnectionError as conn_err:
        print(f"An Connection Error Occured: {conn_err}")
    except Timeout as t_err:
        print(f"An Timeout Error Occured: {t_err}")
    except RequestException as err:
        print(f"An Ambiguous Error Occured: {err}")

def display_user_activity():
    with open(PATH, "r") as file:
        DATA =  json.load(file)

    print("Output: ", end="\n")
    for event in DATA:
        repo_name = event["repo"]["name"]
        if event["type"] == "PushEvent":
            if "commits" in event["payload"]:
                commits = len(event["payload"]["commits"])
                print(f" - Pushed {commits} to {repo_name}")
            else:
                print(f" - Pushed commits to {repo_name}")
        elif event["type"] == "IssuesEvent":
            action = event["payload"]["action"]
            if action == "opened":
                print(f" - Opened a new issue in {repo_name}")
            if action == "closed":
                print(f" - Closed an issue in {repo_name}")
        elif event["type"] == "WatchEvent":
            print(f" - Starred {repo_name}")
        elif event["type"] == "PullRequestEvent":
            action = event["payload"]["action"]
            if action == "opened":
                print(f" - Opened a pull request in {repo_name}")
            if action == "closed":
                print(f" - Closed a pull request in {repo_name}")
        elif event["type"] == "ForkEvent":
            print(f" - Forked {repo_name}")
        elif event["type"] == "CreateEvent":
            ref_type = event["payload"]["ref_type"]   # branch / repo / tag
            print(f" - Created a {ref_type} in {repo_name}")
        elif event["type"] == "DeleteEvent":
            ref_type = event["payload"]["ref_type"]
            print(f" - Deleted a {ref_type} in {repo_name}")
        elif event["type"] == "IssueCommentEvent":
            print(f" - Commented on an issue in {repo_name}")
        elif event["type"] == "PullRequestReviewCommentEvent":
            print(f" - Commented on a pull request in {repo_name}")

if __name__ == "__main__":
    while True:
        username: str = input("github-activity ")
        if username != "Quit":
            get_user_activity(username=username)
            display_user_activity()
        else:
            break