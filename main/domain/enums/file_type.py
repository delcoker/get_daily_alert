from enum import Enum


class FileType(str, Enum):
    EXCEL = 'excel'
    CSV = 'csv'
    JSON = 'json'
