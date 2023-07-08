from eclipse_todo.helpers.connection import conn
from eclipse_todo.helpers.decorators import (
    guard_conn,
    key_error_handler,
)
from eclipse_todo.helpers.settings import get_settings

from .common import TodoEntry


@key_error_handler
def table():
    return get_settings()['table']


class Todos:
    __table = table()

    @classmethod
    @guard_conn
    def count(cls):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(f'SELECT COUNT(*) FROM {cls.__table};')
                return cur.fetchone()[0]

    @classmethod
    @guard_conn
    def create(cls, todo: TodoEntry):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(
                    f'INSERT INTO {cls.__table} (todo, due) VALUES (%s, %s);',
                    [todo.todo, todo.due],
                )
            connection.commit()

    @classmethod
    @guard_conn
    def get_many(cls, **kwargs):
        sort = kwargs.get('sort') or 1
        skip = kwargs.get('skip') or 0
        limit = kwargs.get('limit') or 25

        sort = "ASC" if sort == 1 else "DESC"
        query = f'SELECT * FROM {cls.__table} ORDER BY id {sort} LIMIT %s OFFSET %s'

        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(query, (limit, skip))
                return cur.fetchall()

    @classmethod
    @guard_conn
    def update(cls, id: int, new_todo: str):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(
                    f'UPDATE {cls.__table} SET todo=%s WHERE id=%s;', [new_todo, id]
                )
            connection.commit()

    @classmethod
    @guard_conn
    def delete(cls, id: int):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(f'DELETE FROM {cls.__table} WHERE id=%s', [id])
            connection.commit()
