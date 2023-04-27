from abc import ABC, abstractmethod


class AuthenticatedRequestRepository(ABC):

    @abstractmethod
    def make_request(self, url, method='GET', headers=None, data=None, json=None, params=None):
        pass
