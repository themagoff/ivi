import os
from dotenv import load_dotenv, find_dotenv
import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response


class RestApi:
    load_dotenv(find_dotenv())
    password = os.getenv('PASSWORD')
    email = os.getenv('EMAIL')
    auth = HTTPBasicAuth(username=email, password=password)
    path = 'http://rest.test.ivi.ru/v2/'

    def get_characters(self) -> Response:
        url = self.path + 'characters'
        return requests.get(url=url, auth=self.auth)

    def get_character(self, name: str = None) -> Response:
        url = self.path + 'character'
        params = {'name': name}
        return requests.get(url=url, auth=self.auth, params=params)

    def create_character(self, json: dict = None) -> Response:
        url = self.path + 'character'
        return requests.post(url=url, auth=self.auth, json=json)

    def update_character(self, json: dict = None) -> Response:
        url = self.path + 'character'
        return requests.put(url=url, auth=self.auth, json=json)

    def delete_character(self, name: str = None) -> Response:
        url = self.path + 'character'
        params = {'name': name}
        return requests.delete(url=url, auth=self.auth, params=params)

    def reset_collection(self) -> Response:
        url = self.path + 'reset'
        return requests.post(url=url, auth=self.auth)
