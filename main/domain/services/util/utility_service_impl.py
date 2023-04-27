import datetime
import re
import datetime as dt
from inspect import getframeinfo, stack

import functional as pyfunctional
import pandas as pd
from pandas import DataFrame

from main.domain.enums.dilation_type import DilationType

try:
    # python2
    # import __builtin__
    import builtins as __builtin__
except ImportError:
    # python3
    import builtins as __builtin__


class UtilityServiceImpl:
    def __int__(self):
        pass

    @staticmethod
    def convert_to_float(num):
        try:
            return float(num)
        except ValueError:
            return 0.0

    @staticmethod
    def convert_percent(num):
        try:
            return UtilityServiceImpl.convert_to_float(num) / 100
        except ValueError:
            return 0.0

    @staticmethod
    def replace_percent_symbol(self, num):
        try:
            return self.replace("%", "")
        except AttributeError:
            return self

    @staticmethod
    def extract_digits(x):
        try:
            absolute_number = re.sub("[^0-9.]", "", x)
            return absolute_number if "-" not in x else -float(absolute_number)
        except TypeError:
            return x

    @staticmethod
    def get_today():
        return dt.date.today()

    @staticmethod
    def join_how(left_df, right_df):
        return "left" if len(left_df) > len(right_df) else "right"

    @staticmethod
    def get_month_name(month: int):
        if month == 0:
            month = 12
        datetime_object = dt.datetime.strptime(str(int(month)), "%m")
        month_name = datetime_object.strftime("%b")
        return month_name

    @staticmethod
    def convert_js_date(date_string: str):
        try:
            date_str = str(date_string)
            date_str = re.sub(r'\([\s\S]*\)', "", date_str)
            date_str = date_str.strip()
            date_str = dt.datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S %Z%z")

            return date_str
        except ValueError:
            return UtilityServiceImpl.convert_regular_date(date_string)

    @staticmethod
    def convert_regular_date(date_string: str):
        try:
            return pd.to_datetime(date_string, errors='coerce')
        except ValueError:
            return ''

    @staticmethod
    def insert_row(df_to_insert_into: DataFrame, value_to_insert, column_name):

        starting_position = df_to_insert_into.head(1).copy()
        starting_position.at[starting_position.first_valid_index(), column_name] = value_to_insert

        df_to_insert_into = pd.concat([pd.DataFrame(starting_position), df_to_insert_into], ignore_index=True)

        print("Trying to insert starting position value\n", starting_position)
        return df_to_insert_into

    @staticmethod
    def get_forecast_merge_df(start_date, end_date, dilation_type, metric_data_frame):
        date_segment_merge_cols = UtilityServiceImpl.get_date_segment_column(list(metric_data_frame.columns), DilationType.YEAR.value)[
            0]  # try to merge on non-null/nan l8r
        forecast_merge_columns_left = [DilationType.YEAR.value]

        if dilation_type == DilationType.QUARTER:
            date_segment_merge_cols = [UtilityServiceImpl.get_date_segment_column(list(metric_data_frame.columns), DilationType.YEAR.value)[0],
                                       UtilityServiceImpl.get_date_segment_column(list(metric_data_frame.columns), DilationType.QUARTER.value)[0]]
            forecast_merge_columns_left = [DilationType.YEAR.value, DilationType.QUARTER.value]

        if dilation_type == DilationType.MONTH:
            date_segment_merge_cols = [UtilityServiceImpl.get_date_segment_column(list(metric_data_frame.columns), DilationType.YEAR.value)[0],
                                       UtilityServiceImpl.get_date_segment_column(list(metric_data_frame.columns), DilationType.QUARTER.value)[0],
                                       UtilityServiceImpl.get_date_segment_column(list(metric_data_frame.columns), DilationType.MONTH.value)[0],
                                       ]
            forecast_merge_columns_left = [DilationType.YEAR.value, DilationType.QUARTER.value, DilationType.MONTH.value]

        forcaster_df = UtilityServiceImpl.dilation_forecaster_df(start_date, end_date, dilation_type)

        merged_df = forcaster_df.merge(metric_data_frame, how='left',
                                       left_on=forecast_merge_columns_left,
                                       right_on=date_segment_merge_cols, suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
        return merged_df

    @staticmethod
    def get_date_segment_column(lst, date_segment_identifier):
        return [string for string in lst if date_segment_identifier.casefold() in string.casefold()]

    @staticmethod
    def dilation_forecaster_df(start_date, end_date, dilation_type: DilationType):
        if dilation_type == DilationType.YEAR:
            start_year = datetime.datetime.strptime(start_date, "%Y-%m-%d").year
            last_year = (datetime.datetime.strptime(end_date, "%Y-%m-%d") + dt.timedelta(days=+28)).year

            forecast_list = list()
            for year in range(start_year, last_year):
                forecast_list.append([year])

            forecast = pd.DataFrame(forecast_list)
            forecast.columns = ['Year']

            return forecast

        if dilation_type == DilationType.QUARTER:
            s_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
            e_date = dt.datetime.strptime(end_date, "%Y-%m-%d") + dt.timedelta(days=+28)
            forecast = pd.date_range(s_date, e_date - dt.timedelta(days=0), freq='m')

            forecast = pd.DataFrame(forecast)
            forecast.columns = ['Date']
            forecast['Year'] = forecast['Date'].dt.year
            forecast['Quarter'] = forecast['Date'].dt.quarter.apply(lambda x: 'Q' + str(x).replace('.0', ''))
            forecast = forecast[['Year', 'Quarter']].drop_duplicates()

            return forecast

        if dilation_type == DilationType.MONTH:
            s_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
            e_date = dt.datetime.strptime(end_date, "%Y-%m-%d") + dt.timedelta(days=+28)
            forecast = pd.date_range(s_date, e_date - dt.timedelta(days=1), freq='m')

            forecast = pd.DataFrame(forecast)
            forecast.columns = ['Date']
            forecast['Year'] = forecast['Date'].dt.year
            forecast['Quarter'] = forecast['Date'].dt.quarter.apply(lambda x: 'Q' + str(x).replace('.0', ''))
            forecast['Month'] = forecast['Date'].dt.month

            return forecast

def print(*args, **kwargs):
    caller = getframeinfo(stack()[1][0])
    # __builtin__.print('New print function')
    return __builtin__.print("%s:%d ::%s:=" % (caller.filename, caller.lineno, datetime.datetime.now()), *args, **kwargs)
