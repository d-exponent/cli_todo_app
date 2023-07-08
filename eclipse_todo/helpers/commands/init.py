from eclipse_todo.helpers.connection import conn
from eclipse_todo.helpers.decorators import guard_conn


@guard_conn
def create_table(table, pg: bool, mysql: bool):
    with conn() as connection:
        with connection.cursor() as cursor:
            pg_query = f"""
                  CREATE TABLE {table} (
                      id SERIAL PRIMARY KEY,
                      todo VARCHAR(140) NOT NULL,
                      due DATE,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  );"""

            mysql_query = f"""
                  CREATE TABLE {table} (
                      id INT NOT NULL AUTO_INCREMENT,
                      todo VARCHAR(140) NOT NULL,
                      due DATE,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      PRIMARY KEY ( id )
                  );"""

            cursor.execute(pg_query if pg else mysql_query if mysql else '')
