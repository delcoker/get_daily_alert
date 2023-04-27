import pandas as pd

from main.application.services.daily_alert_service import DailyAlertService
from main.domain.repositories.authenticated_request_repository import AuthenticatedRequestRepository
from main.domain.services.food_security_service import FoodSecurityService

url_food_security = "https://api.hungermapdata.org/swe-notifications/foodsecurity"


class DailyAlertServiceImpl(DailyAlertService):

    def __init__(self,
                 authenticated_request_repository: AuthenticatedRequestRepository,
                 food_security_service: FoodSecurityService
                 ):
        self.authenticated_request_repository = authenticated_request_repository
        self.food_security_service = food_security_service

    def get_alert_data(self):
        regions_food_security_list = self.authenticated_request_repository.make_request(
            url=url_food_security,
            headers={'Content-Type': 'application/json'},
            json={'result': {}}
        )

        params = {'days_ago': 30}
        regions_food_security_list_30_days_ago = self.authenticated_request_repository.make_request(
            url=url_food_security,
            headers={'Content-Type': 'application/json'},
            params=params
        )

        regions_food_security_df = pd.DataFrame(regions_food_security_list)
        regions_food_security_df_30_days_ago = pd.DataFrame(regions_food_security_list_30_days_ago)
        regions_food_security_df_30_days_ago.rename(columns={"food_insecure_people": "food_insecure_people_30_days_ago"}, inplace=True)

        food_security_df = self.food_security_service.get_alerts(regions_food_security_df, regions_food_security_df_30_days_ago)

        return food_security_df.to_json(orient="records")
