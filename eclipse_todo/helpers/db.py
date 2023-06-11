from psycopg2 import connect
from eclipse_todo.helpers.settings import get_settings


def conn(db_settings: dict = get_settings()['database']):
    return connect(
        database=db_settings.get('name'),
        user=db_settings.get('user'),
        password=db_settings.get('password'),
        host=db_settings.get('host'),
        port=db_settings.get('port'),
    )


def close_connection(conn):
    if conn is not None:
        conn.close()