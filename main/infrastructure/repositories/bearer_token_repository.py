from abc import ABC, abstractmethod


class BearerTokenRepository(ABC):

    @abstractmethod
    def get_bearer_token(self):
        pass
