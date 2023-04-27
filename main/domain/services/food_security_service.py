from abc import ABC, abstractmethod


class FoodSecurityService(ABC):

    @abstractmethod
    def get_alerts(self, df_now, df_30_years_ago):
        pass
