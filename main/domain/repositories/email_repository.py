from abc import ABC, abstractmethod


class EmailRepository(ABC):

    @abstractmethod
    def send_email(self, to_email_list, subject, body):
        pass
