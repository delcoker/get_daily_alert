"""Container module."""
import os

import pandas as pd

from main.application.services.daily_alert_service_impl import DailyAlertServiceImpl
from main.infrastructure.repositories.authenticated_request_repository_impl import AuthenticatedRequestRepositoryImpl
from main.infrastructure.repositories.bearer_token_repository_impl import BearerTokenRepositoryImpl

pd.set_option('display.width', 500)
pd.set_option("display.max_columns", 20)

username = os.getenv('username')
password = os.getenv('password')
bearer_token_url = os.getenv('bearer_token_url')

region_country_df = pd.read_csv('datasets/region_country_data.csv')
region_population_df = pd.read_csv('datasets/population.csv')
email_country_df = pd.read_csv('datasets/email_per_country.csv')

# Repository

bearer_token_repository = BearerTokenRepositoryImpl(username, password, bearer_token_url)

authenticated_request_repository = AuthenticatedRequestRepositoryImpl(bearer_token_repository)

# Services

daily_alert_service = DailyAlertServiceImpl(authenticated_request_repository=authenticated_request_repository,
                                            region_country_df=region_country_df,
                                            region_population_df=region_population_df,
                                            email_country_df=email_country_df)
