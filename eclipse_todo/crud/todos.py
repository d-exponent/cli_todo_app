from datetime import datetime
from eclipse_todo.helpers.database import conn, guard_conn


class Todos:
    @classmethod
    @guard_conn
    def count(cls):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('SELECT COUNT(*) FROM todos;')
                return cur.fetchone()[0]

    @classmethod
    @guard_conn
    def create(cls, params: list | tuple):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('INSERT INTO todos (todo, due) VALUES (%s, %s);', params)
                connection.commit()

    @classmethod
    @guard_conn
    def get_many(cls, **kwargs):
        sort = kwargs.get('sort') or 1
        skip = kwargs.get('skip') or 0
        limit = kwargs.get('limit') or 25

        sort = "ASC" if sort == 1 else "DESC"
        query = f'SELECT * FROM todos ORDER BY id {sort} LIMIT %s OFFSET %s'

        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(query, (limit, skip))
                return cur.fetchall()

    @classmethod
    @guard_conn
    def update_by_id(cls, content: str, todo_id: int):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('UPDATE todos SET todo=%s WHERE id=%s;', [content, todo_id])
                connection.commit()

    @classmethod
    @guard_conn
    def delete_by_id(cls, todo_id: int):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('DELETE FROM todos WHERE id=%s', [todo_id])
                connection.commit()

    @classmethod
    @guard_conn
    def delete_by_created_at(cls, created_at: datetime):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('DELETE FROM todos WHERE created_at=%s', [created_at])
                connection.commit()

    @classmethod
    @guard_conn
    def delete_by_due(cls, due: datetime):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('DELETE FROM todos WHERE due=%s', [due])
                connection.commit()
