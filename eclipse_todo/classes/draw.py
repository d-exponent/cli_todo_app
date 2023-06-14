import csv
from rich import box
from rich.console import Console
from dataclasses import dataclass

from eclipse_todo import constants as c
from eclipse_todo.helpers.db import conn
from eclipse_todo.helpers.utils import new_line_then_print, new_line
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
            new_line_then_print("Todo list is currently empty.")
            new_line_then_print(c.CREATE_TODO)

    def db_todos(self) -> None:
        table = create_set_columns('todos', {'title': "Database Todos"})
        try:
            with conn() as connection:
                with connection.cursor() as cur:
                    cur.execute('SELECT * FROM todos')
                    rows = cur.fetchall()

            if len(rows) == 0:
                new_line_then_print("Todo list is currently empty.")
                new_line_then_print(c.CREATE_TODO)
                return

            # We have rows here
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
            new_line_then_print("You currently have no set database credentials")
            new_line()
            self._console.print(table)
            new_line_then_print(c.CONFIG_DB_COMMAND)
            new_line()
            return

        try:
            table.add_row(
                db_settings['name'],
                db_settings['user'],
                db_settings['password'],
                db_settings['host'],
                str(db_settings['port']),
            )
            self._console.print(table)
        except KeyError as e:
            print(f'🛑 KeyError: There is no {e} set in your database configuration')
            new_line_then_print(c.CONFIG_DB_COMMAND)


draw = Draw()
