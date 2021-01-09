import requests
# import json
import os
from dotenv import load_dotenv
load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')


def headers():
    header = {"Authorization": f"Bearer {bearer_token}"}
    return header


def search_req(header, query):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}"
    res = requests.get(url, headers=header).json()
    data = []
    for data_id in res['data']:
        data.append(data_id['text'])
    return data


def main():
    header = headers()
    data = search_req(header, 'infosec')
    for tweet in data:
        print(tweet+'\n')

if __name__ == '__main__':
    main()
