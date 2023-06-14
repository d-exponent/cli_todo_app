from psycopg2.extensions import connection
from eclipse_todo.helpers.database import conn


def test_app_database_credentials():
    assert type(conn()) == connection
