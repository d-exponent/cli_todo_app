import psycopg2 as postgres
import mysql.connector as mysql

from eclipse_todo.helpers.settings import get_settings
from .decorators import file_not_found_handler


@file_not_found_handler
def conn(db_settings: dict = None):
    settings = db_settings if db_settings else get_settings()
    db_type = settings['type']
    connect = postgres.connect if db_type == 'postgres' else mysql.connect
    del settings['type']
    del settings['table']
    return connect(**settings)
