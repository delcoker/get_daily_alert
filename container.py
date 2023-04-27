"""Container module."""
import os

import pandas as pd

from main.application.services.daily_alert_service_impl import DailyAlertServiceImpl
from main.domain.services.food_security_service_impl import FoodSecurityServiceImpl
from main.infrastructure.repositories.authenticated_request_repository_impl import AuthenticatedRequestRepositoryImpl
from main.infrastructure.repositories.bearer_token_repository_impl import BearerTokenRepositoryImpl
from main.infrastructure.repositories.email_repository_impl import EmailRepositoryImpl

pd.set_option('display.width', 500)
pd.set_option("display.max_columns", 20)

USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')
BEARER_TOKEN_URL = os.getenv('bearer_token_url')

MAIL_HOST = os.getenv("mail_host")
MAIL_PORT = os.getenv('mail_port')
MAIL_USERNAME = os.getenv("mail_username")
MAIL_PASSWORD = os.getenv('mail_password')

region_country_df = pd.read_csv('datasets/region_country_data.csv')
region_population_df = pd.read_csv('datasets/population.csv')
email_country_df = pd.read_csv('datasets/email_per_country.csv')

# Repositories

bearer_token_repository = BearerTokenRepositoryImpl(USERNAME, PASSWORD, BEARER_TOKEN_URL)

authenticated_request_repository = AuthenticatedRequestRepositoryImpl(bearer_token_repository)

email_repository = EmailRepositoryImpl(MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD)

# Services

food_security_service = FoodSecurityServiceImpl(email_repository=email_repository,
                                                region_country_df=region_country_df,
                                                region_population_df=region_population_df,
                                                email_country_df=email_country_df,
                                                )

daily_alert_service = DailyAlertServiceImpl(authenticated_request_repository=authenticated_request_repository,
                                            food_security_service=food_security_service, )
