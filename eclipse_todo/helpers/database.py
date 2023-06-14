from typing import Callable
from psycopg2 import connect, OperationalError, DatabaseError

from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.utils import new_line_then_print
from eclipse_todo.constants import PG_DATABASE_ERR, PG_OPERATIONAL_ERR, CREATE_TODO


def conn(db_settings: dict = get_settings()['database']):
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
            conn_func(*args, **kwargs)
        except OperationalError:
            new_line_then_print(PG_OPERATIONAL_ERR)
        except DatabaseError:
            new_line_then_print(PG_DATABASE_ERR)

    return wrapper


@exec_conn
def draw_db_todos(instance, table):
    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute('SELECT * FROM todos;')
            rows = cur.fetchall()

        if len(rows) == 0:
            new_line_then_print("Todo list is currently empty.")
            new_line_then_print(CREATE_TODO)
        else:
            for i, row in enumerate(rows):
                to_add = (str(i), row[0], str(row[1]), str(row[2]).split('.')[0])
                table.add_row(*to_add)

            instance.console.print(table)


@exec_conn
def add_db_todo(params: list):
    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute('INSERT INTO todos (todo, due) VALUES (%s, %s);', params)
            connection.commit()
