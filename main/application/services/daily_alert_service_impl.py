import json
from io import StringIO

import pandas as pd
from pandas import DataFrame

from main.application.services.daily_alert_service import DailyAlertService
from main.infrastructure.repositories.authenticated_request_repository import AuthenticatedRequestRepository


# A COUNTRY IS MADE UP OF SEVERAL REGIONS

class DailyAlertServiceImpl(DailyAlertService):

    def __init__(self, authenticated_request_repository: AuthenticatedRequestRepository,
                 region_country_df: DataFrame,
                 region_population_df: DataFrame,
                 email_country_df: DataFrame):
        self.authenticated_request_repository = authenticated_request_repository
        self.region_country_df = region_country_df
        self.region_population_df = region_population_df
        self.email_country_df = email_country_df

    def get_food_security(self, df, df_30):
        security = df.merge(df_30)
        security = security.merge(self.region_country_df, how='left', on='region_id')
        security = security.merge(self.region_population_df, how='left')
        # sum regions values of populations in the same country
        concatenated_regions = security.groupby('country_id')['region_id'].apply(lambda x: self.get_region_ids(x)).reset_index()
        security_by_country = security.drop('region_id', axis=1).groupby('country_id').sum().reset_index()
        security_by_country = security_by_country.merge(concatenated_regions)
        #
        security_by_country['percentage_difference'] = (security_by_country["food_insecure_people"] - security_by_country["food_insecure_people_30_days_ago"]) / security_by_country['population'] * 100
        security_by_country['>=5%'] = security_by_country['percentage_difference'] >= 5
        security_by_country = security_by_country[security_by_country['>=5%'] == True]

        security_with_email = security_by_country.merge(self.email_country_df)
        return security_with_email

    def get_region_ids(self, x):
        regions = x.tolist()
        regions_str = [str(region) for region in regions]
        return '-'.join(regions_str)

    def get_alert_data(self):
        # •	Food security (expressed as total number of food-insecure people in each region) is available in a REST API
        # o	GET https://api.hungermapdata.org/swe-notifications/foodsecurity returns a list of results (one per region),
        # each containing the id of the region and the number of food insecure people

        regions_food_security_list = self.authenticated_request_repository.make_request(
            url='https://api.hungermapdata.org/swe-notifications/foodsecurity',
            headers={'Content-Type': 'application/json'},
            json={'result': {}}
        )

        params = {'days_ago': 30}
        regions_food_security_list_30_days_ago = self.authenticated_request_repository.make_request(
            url='https://api.hungermapdata.org/swe-notifications/foodsecurity',
            headers={'Content-Type': 'application/json'},
            params=params
        )

        regions_food_security_df = pd.DataFrame(regions_food_security_list)
        regions_food_security_df_30_days_ago = pd.DataFrame(regions_food_security_list_30_days_ago)
        regions_food_security_df_30_days_ago.rename(columns={"food_insecure_people": "food_insecure_people_30_days_ago"}, inplace=True)

        food_security_df = self.get_food_security(regions_food_security_df, regions_food_security_df_30_days_ago)




        # # o	GET https://api.hungermapdata.org/swe-notifications/country/{country_id}/regions
        # # returns the list of regions for a given country
        #
        # country_regions_list = self.authenticated_request_repository.make_request(
        #     url='https://api.hungermapdata.org/swe-notifications/country/{country_id}/regions',
        #     headers={'Content-Type': 'application/json'}
        # )

        food_security_json = food_security_df.to_json()

        return food_security_json

    @staticmethod
    def save_locally(russ_metric_data_serialized):
        with open('zIgnoredFolder/russ_csv.js', 'w') as f:
            data = json.loads(russ_metric_data_serialized)
            json.dump(data, f)

    @staticmethod
    def get_csv_file_body(json_obj):
        df = pd.read_json(json_obj)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        return csv_buffer.getvalue()
