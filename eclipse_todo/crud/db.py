from psycopg2 import connect

conn = connect(
    database="<Your database>", user="postgres", password="<Your password>", port="5432"
)


class DbTodos:
    @classmethod
    def connect():
        pass
