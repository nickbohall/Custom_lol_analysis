import re
from base64 import b64encode

import requests
import urllib3

# Disabling warnings
urllib3.disable_warnings()

# Lockfile path
lockfile_content = "LeagueClient:24472:64015:HhnwNbdLHUNy3-Ubsi0zKg:https"

# Define the regex pattern
lockfile_pattern = r'[^:]+:[^:]+:(\d+):([^:]+):[^:]+'

# Match the pattern in the lockfile content
match = re.match(lockfile_pattern, lockfile_content)

# Extract port number and password
port_number = match.group(1)
password = match.group(2)
username = "riot"
puuid = 'de0e96ce-759a-5607-b308-44382e0ab8b0'
tag_line = 3654


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


# Authorization
headers = {'Authorization': basic_auth(username, password)}


def get_match_history_summoner(puuid):
    url = f'https://127.0.0.1:{port_number}/lol-match-history/v1/products/lol/{puuid}/matches'

    response = requests.get(url, headers=headers,
                            verify=False)  # Note: Disabling SSL verification for a self-signed certificate
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Status Code: {response.status_code}")
        raise ValueError("The pull did not succeed")


def get_game_history(game_id):
    url = f'https://127.0.0.1:{port_number}/lol-match-history/v1/games/{game_id}'

    response = requests.get(url, headers=headers,
                            verify=False)  # Note: Disabling SSL verification for a self-signed certificate
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Status Code: {response.status_code}")
        raise ValueError("The pull did not succeed")


def get_current_summoner():
    url = f'https://127.0.0.1:{port_number}/lol-summoner/v1/current-summoner'

    response = requests.get(url, headers=headers,
                            verify=False)  # Note: Disabling SSL verification for a self-signed certificate

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Status Code: {response.status_code}")
        raise ValueError("The current summoner pull did not succeed")


def get_puuid(alias, tag_line):
    url = f'https://127.0.0.1:{port_number}/lol-summoner/v1/alias/lookup'
    params = {'gameName': alias,
              'tagLine': tag_line}

    response = requests.get(url, headers=headers, params=params,
                            verify=False)  # Note: Disabling SSL verification for a self-signed certificate

    if response.status_code == 200:
        data = response.json()
        return data['puuid']
    else:
        print(f"Status Code: {response.status_code}")
        raise ValueError("The get_puuid pull did not succeed")


def find_champion(championId):
    url = f'https://127.0.0.1:lol-champ-select/v1/all-grid-champions'

    response = requests.get(url, headers=headers,
                            verify=False)  # Note: Disabling SSL verification for a self-signed certificate

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Status Code: {response.status_code}")
        raise ValueError("The find_champion pull did not succeed")
