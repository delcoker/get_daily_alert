from abc import ABC, abstractmethod


class DailyAlertService(ABC):

    @abstractmethod
    def get_alert_data(self):
        pass
