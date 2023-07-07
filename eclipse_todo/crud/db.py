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
    def update(cls, id: int, new_todo: str):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('UPDATE todos SET todo=%s WHERE id=%s;', [new_todo, id])
                connection.commit()

    @classmethod
    @guard_conn
    def delete(cls, id: int):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('DELETE FROM todos WHERE id=%s', [id])
                connection.commit()
