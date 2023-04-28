import requests

from main.domain.repositories.authenticated_request_repository import AuthenticatedRequestRepository


class AuthenticatedRequestRepositoryImpl(AuthenticatedRequestRepository):

    def __init__(self, token_repository):
        self.token_repository = token_repository

    def make_request(self, url, method='GET', headers=None, data=None, json=None, params=None):
        bearer_token = self.token_repository.get_bearer_token()

        headers = headers or {}
        headers['Authorization'] = f'Bearer {bearer_token}'

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            json=json
        )

        if response.status_code >= 400:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        return response.json()
