from eclipse_todo.helpers.database import conn, exec_conn


class Database:
    @classmethod
    @exec_conn
    def create(cls, params: list | tuple):
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute('INSERT INTO todos (todo, due) VALUES (%s, %s);', params)
                connection.commit()

    @classmethod
    @exec_conn
    def read(cls, sort, skip: int = 0, limit: int = 50):
        sort = "ASC" if sort and sort == 1 else "DESC"
        with conn() as connection:
            with connection.cursor() as cur:
                cur.execute(
                    f'SELECT * FROM todos ORDER BY id {sort} LIMIT %s OFFSET %s',
                    [limit, skip],
                )
                return cur.fetchall()
