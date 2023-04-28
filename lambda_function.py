import os

import functional as pyfunctional
import pandas as pd

import container
from main.application.services.daily_alert_service import DailyAlertService
from main.infrastructure.repositories.authenticated_request_repository_impl import AuthenticatedRequestRepositoryImpl
from main.infrastructure.repositories.bearer_token_repository_impl import BearerTokenRepositoryImpl


def lambda_handler(event, context, daily_alert_service: DailyAlertService = container.daily_alert_service):
    # RUN ONCE A YEAR
    # get_region_country_data()
    # get_region_country_data_joined()

    alert_data = daily_alert_service.get_alert_data()

    return {
        'statusCode': 200,
        'body': alert_data,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }


def get_region_country_data_joined():
    directory = './'
    prefix = 'country_data'

    dfs = []

    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            dfs.append(df)

    country_data_df = pd.concat(dfs, axis=0)
    country_data_df.to_csv(f'region_country_data.csv', index=False)


def get_region_country_data():
    username = os.getenv('username')
    password = os.getenv('password')
    bearer_token_url = os.getenv('bearer_token_url')

    # read csv to get regions
    population_df = pd.read_csv('datasets/population.csv')
    region_ids = population_df['region_id'].tolist()

    # o	GET https://api.hungermapdata.org/swe-notifications/region/{region_id}/country
    # returns country information for a given region

    total_requests_per_token = 200
    start_position = 0  # if bearer expires, insert last i value

    for i in range(start_position + total_requests_per_token, len(region_ids)):
        if i % total_requests_per_token == 0:
            bearer_token_reset = BearerTokenRepositoryImpl(username, password, bearer_token_url)
            authenticated_request_repository_reset = AuthenticatedRequestRepositoryImpl(bearer_token_reset)

            country_info_list = pyfunctional.seq(region_ids[i:i + total_requests_per_token]).map(
                lambda region_id: authenticated_request_repository_reset.make_request(
                    url=f'https://api.hungermapdata.org/swe-notifications/region/{region_id}/country',
                    headers={'Content-Type': 'application/json'}
                )).list()

            country_list_df = pd.DataFrame(country_info_list)

            country_list_df.to_csv(f'country_data{i}.csv', index=False)


def get_request_params(event, param):
    return event["queryStringParameters"][param]


def get_request_body(event):
    try:
        request_body = event["body"]
        return request_body
    except Exception:
        raise Exception("Request does not have a body!!!")
