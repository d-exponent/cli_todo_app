from psycopg2 import connect
from .settings import get_settings
from eclipse_todo.constants import SETTINGS_FILE


def conn():
    db_cred = get_settings()['database']
    return connect(
        database=db_cred.get('name'),
        user=db_cred.get('user'),
        password=db_cred.get('password'),
        host=db_cred.get('host'),
        port=db_cred.get('port'),
    )
