import csv
from rich import box
from rich.console import Console
from dataclasses import dataclass

from eclipse_todo import constants as c
from eclipse_todo.helpers.db import conn
from psycopg2 import OperationalError, DatabaseError
from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.table import create_set_columns, handle_db_err_msg


@dataclass
class Draw:
    _console: Console = Console()

    def csv_todos(self) -> None:
        table = create_set_columns('todos', {'title': "CSV Todos"})
        try:
            with open(c.TODOS_FILE, 'r') as data:
                for i, row in enumerate(csv.reader(data)):
                    if i != 0:
                        table.add_row(*row)
                self._console.print(table)
        except FileNotFoundError:
            print("\nTodo list is currently empty.\n" + c.CREATE_TODO)

    def db_todos(self) -> None:
        table = create_set_columns('todos', {'title': "Database Todos"})
        try:
            with conn() as connection:
                with connection.cursor() as cur:
                    cur.execute('SELECT * FROM todos')
                    rows = cur.fetchall()

            if len(rows) == 0:
                print("\nTodo list is currently empty.\n" + c.CREATE_TODO)
            else:
                for i, row in enumerate(rows):
                    to_add = (str(i), row[0], str(row[1]), str(row[2]).split('.')[0])
                    table.add_row(*to_add)

        except OperationalError:
            handle_db_err_msg(c.PG_OPERATIONAL_ERR)
            self.db_settings()

        except DatabaseError:
            handle_db_err_msg(c.PG_DATABASE_ERR)
            self.db_settings()
        else:
            self._console.print(table)

    def db_settings(self) -> None:
        config = {'title': "Database Settings", 'box': box.HORIZONTALS}
        table = create_set_columns('settings', config)
        db_settings = get_settings()['database']

        if not db_settings:
            print("\nYou currently have no set database credentials\n")
            self._console.print(table)
            print("\n" + c.CONFIG_DB_COMMAND + "\n")
            return

        table.add_row(
            db_settings['name'],
            db_settings['user'],
            db_settings['password'],
            db_settings['host'],
            str(db_settings['port']),
        )
        self._console.print(table)


draw = Draw()
