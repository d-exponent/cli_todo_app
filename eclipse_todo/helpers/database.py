from typing import Callable
from psycopg2 import connect, OperationalError, DatabaseError

from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.utils import new_line_then_print
from eclipse_todo.constants import PG_DATABASE_ERR, PG_OPERATIONAL_ERR

database_settings = get_settings()['database']


def conn(db_settings: dict = database_settings):
    return connect(
        database=db_settings.get('name'),
        user=db_settings.get('user'),
        password=db_settings.get('password'),
        host=db_settings.get('host'),
        port=db_settings.get('port'),
    )


# DECORATOR TO HANDLE OPERATIONAL AND DATABASE ERRORS
def exec_conn(conn_func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return conn_func(*args, **kwargs)
        except OperationalError:
            new_line_then_print(PG_OPERATIONAL_ERR)
        except DatabaseError:
            new_line_then_print(PG_DATABASE_ERR)

    return wrapper
