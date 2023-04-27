import requests

from main.domain.repositories.bearer_token_repository import BearerTokenRepository


class BearerTokenRepositoryImpl(BearerTokenRepository):

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def get_bearer_token(self):

        auth = (self.username, self.password)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'client_credentials'}

        response = requests.post(self.url, headers=headers, auth=auth, data=data)

        if response.status_code == 200:
            token = response.json()['token']
            return f"{token}"
        else:
            print(f"Error: {response.status_code} - {response.json()['error_description']}")
