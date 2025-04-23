import requests
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()  # Load variables from .env

def get_events():
    url = f"{base_url}/users/{username}/events"

    # query_params = {
    #     "sort": "updated",
    #     "per_page": 5
    # }

    headers = {
        "Authorization" : f"Bearer " + os.getenv("API_KEY")
    }

    response = requests.get(url,headers=headers) # params=query_params

    if response.status_code == 200:
        return response.json()
    else:
        return None

def commit_comment_event(data):
    commit_id = data[0]["payload"]["comment"]["commit_id"]
    repo = data[0]["repo"]["name"]
    repo = repo.split("/")[-1] #grab the name only

    url = f"{base_url}/repos/{username}/{repo}/commits/{commit_id}/comments"

    headers = {
        "Authorization" : f"Bearer " + os.getenv("API_KEY"),
    }

    data = {
        "body": f"This is an automated message to troll Liam"
    }

    status_code = requests.post(url, headers=headers, json=data).status_code

    return status_code

def issue_comment_event(data):
    issue_number = data[0]["payload"]["issue"]["number"]
    repo = data[0]["repo"]["name"]
    repo = repo.split("/")[-1] #grab the name only

    url = f"{base_url}/repos/{username}/{repo}/issues/{issue_number}/comments"

    headers = {
        "Authorization" : f"Bearer " + os.getenv("API_KEY"),
    }

    data = {
        "body": f"This is an automated message to troll Liam"
    }

    status_code = requests.post(url, headers=headers, json=data).status_code

    return status_code

def pull_request_comment_event(data):
    pull_number = data[0]["payload"]["issue"]["number"]

    repo = data[0]["repo"]["name"]
    repo = repo.split("/")[-1] #grab the name only


    url = f"{base_url}/repos/{username}/{repo}/pulls/{pull_number}/comments"

    headers = {
        "Authorization" : f"Bearer " + os.getenv("API_KEY"),
    }

    data = {
        "body": f"This is an automated message to troll Liam"
    }

    status_code = requests.post(url, headers=headers, json=data).status_code

    return status_code

#json_parsed_to_dictionary = json.loads(json_string) #converts string to python dictionary
#pretty_json_string = json.dumps(json_parsed_to_dictionary, indent=4, sort_keys=True) #formats python dictionary to string
#print(pretty_json)


username = "JDgoldvox" #LGugs3
base_url = f"https://api.github.com"
commented = False
last_id = -1

while True :

    #Delay for API calls
    time.sleep(5)

    #Get latest data
    event_data = get_events()

    if event_data == None :
        print("ERROR")

    #get latest event
    event_type = event_data[0]["type"]

    if event_type != "CommitCommentEvent" and event_type != "IssueCommentEvent" and event_type != "PullRequestReviewCommentEvent":
        print("Event not valid: " + event_data[0]["type"])
        continue

    print("writing comment...")

    if event_type == "CommitCommentEvent":
        new_id = event_data[0]["payload"]["comment"]["id"]

    if event_type == "IssueCommentEvent":
        new_id = event_data[0]["payload"]["issue"]["id"]

    if event_type == "PullRequestReviewCommentEvent":
        new_id = event_data[0]["payload"]["review"]["id"]

    #do not write another comment if already commented
    if last_id == new_id:
        continue
    else:
        last_id = new_id


    #comment something on the repo
    code = -1

    if event_type == "CommitCommentEvent":
        code = commit_comment_event(event_data)

    if event_type == "IssueCommentEvent":
        code = issue_comment_event(event_data)

    if event_type == "PullRequestReviewCommentEvent":
        code = pull_request_comment_event(event_data)

    print(code)