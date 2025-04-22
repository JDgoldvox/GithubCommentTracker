import requests
import json

def get_user_repositories():
    url = f"{base_url}/users/{username}/repos"

    query_params = {
        "sort": "updated",
        "per_page": 5
    }

    # headers =
    # {
    #     "Authorization" :
    # }

    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

username = "LGugs3" #LGugs3
base_url = f"https://api.github.com"

json_string = get_user_repositories() #gets json as string
#json_parsed_to_dictionary = json.loads(json_string) #converts string to python dictionary
#pretty_json_string = json.dumps(json_parsed_to_dictionary, indent=4, sort_keys=True) #formats python dictionary to string

#print(pretty_json)

if(json_string != None):
    for repo in json_string:
        print(repo["name"])
else:
    print("Error with request")

