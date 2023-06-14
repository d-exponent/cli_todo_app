import csv
from rich import box
from rich.console import Console
from dataclasses import dataclass

from eclipse_todo.constants import CREATE_TODO, CONFIG_DB_COMMAND, TODOS_FILE
from eclipse_todo.helpers.utils import new_line_then_print, new_line
from eclipse_todo.helpers.database import draw_db_todos
from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.table import create_set_columns


@dataclass
class Draw:
    console: Console = Console()

    def csv_todos(self) -> None:
        table = create_set_columns('todos', {'title': "CSV Todos"})
        try:
            with open(TODOS_FILE, 'r') as data:
                for i, row in enumerate(csv.reader(data)):
                    if i != 0:
                        table.add_row(*row)
                self.console.print(table)
        except FileNotFoundError:
            new_line_then_print("Todo list is currently empty.")
            new_line_then_print(CREATE_TODO)

    def db_todos(self) -> None:
        table = create_set_columns('todos', {'title': "Database Todos"})
        draw_db_todos(self, table)

    def db_settings(self) -> None:
        config = {'title': "Database Settings", 'box': box.HORIZONTALS}
        table = create_set_columns('settings', config)
        db_settings = get_settings()['database']

        if not db_settings:
            new_line_then_print("You currently have no set database credentials")
            new_line()
            self.console.print(table)
            new_line_then_print(CONFIG_DB_COMMAND)
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
            self.console.print(table)
        except KeyError as e:
            print(f'🛑 KeyError: There is no {e} set in your database configuration')
            new_line_then_print(CONFIG_DB_COMMAND)


draw = Draw()
