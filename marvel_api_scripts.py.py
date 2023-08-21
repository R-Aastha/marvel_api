import requests
import pandas as pd
import time
import hashlib
import argparse

class API:

    def __init__(self, headers=None, params=None):
        self.headers = headers or {}
        self.params = params or {}

    def fetch_data(self, url):
        try:
            response = requests.get(url, headers=self.headers, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception("An exception has occured during the API request = ", e)

    def convert_to_dataframe(Self, data):
        try:
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            raise Exception("An error occured while converting data to DataFrame", e)

class MarvelAPI(API):

    base_url = "http://gateway.marvel.com/v1/public"

    def __init__(self, api_key, hash_key, ts):
        params = {
            "apikey": api_key,
            "hash": hash_key,
            "ts": ts
        }

        super().__init__(params=params)

    def fetch_data(self, endpoint, namestartswith=None, length=100):
        url = f"{self.base_url}/{endpoint}"
        self.params["limit"] = length
        if namestartswith:
            self.params["nameStartsWith"] = namestartswith
        return super().fetch_data(url)

    def convert_to_dataframe(self,data):
        return super().convert_to_dataframe(data)


def main():
    parser = argparse.ArgumentParser(description="Marvel API Script")
    parser.add_argument("--apikey", required=True, help="9af3e27a239ff097c6940d45ed0c5a97")

    args = parser.parse_args()

    api_key = args.apikey
    ts = str(int(time.time()))

    private_key = "57bae61d5baffa57e81846ca48646520f15f2ed8"
    data = f"{ts}{private_key}{api_key}".encode()
    hash_key = hashlib.md5(data).hexdigest()

    marvel_api = MarvelAPI(api_key, hash_key, ts)

    data = marvel_api.fetch_data("characters", namestartswith="A", length=100)

    df = marvel_api.convert_to_dataframe(data)

if __name__ == "main":
    main()


