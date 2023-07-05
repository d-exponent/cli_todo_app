import csv
from rich import box
from rich.console import Console
from dataclasses import dataclass

from eclipse_todo.constants import CREATE_TODO, CONFIG_DB_COMMAND, TODOS
from eclipse_todo.helpers.utils import new_line_then_print, new_line
from eclipse_todo.crud.db import Database
from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.table import set_columns


@dataclass
class Draw:
    console: Console = Console()

    def csv_todos(self) -> None:
        table = set_columns('todos', {'title': "CSV Todos"})
        try:
            with open(TODOS, 'r') as data:
                for i, row in enumerate(csv.reader(data)):
                    if i != 0:  # avoid the headers
                        table.add_row(*row)
                new_line()
                self.console.print(table)
                new_line()
        except FileNotFoundError:
            new_line_then_print("Csv todos is currently empty.")
            new_line_then_print(CREATE_TODO)
            new_line()

    def db_todos(
        self, skip: int = 0, limit: int = 50, sort: int = 1, reader: Database = Database
    ) -> None:
        table = set_columns('todos', {'title': "Database Todos"})

        # Write tests for this funtion
        rows = reader.read(sort, skip, limit)
        if len(rows) == 0:
            new_line_then_print("Todo list is currently empty.")
            new_line_then_print(CREATE_TODO)
        else:
            for row in rows:
                to_add = (str(row[0]), row[1], str(row[2]), str(row[3]).split('.')[0])
                table.add_row(*to_add)

        new_line()
        self.console.print(table)
        new_line()

    def settings(self) -> None:
        table = set_columns(
            'settings',
            {'title': "Database Settings.", 'box': box.HORIZONTALS},
        )

        settings = get_settings()
        db_settings, protocol = [settings['database'], settings['protocol']]
        protocol_msg = f'Current Protocol => {protocol}'

        def draw_settings():
            new_line_then_print(protocol_msg)
            new_line()
            self.console.print(table)
            new_line()

        if not settings['database']:
            draw_settings()
            print("You currently have no database settings")
        else:
            table.add_row(
                db_settings.get('name'),
                db_settings.get('user'),
                db_settings.get('password'),
                db_settings.get('host'),
                str(db_settings.get('port')),
            )
            draw_settings()

        print(CONFIG_DB_COMMAND)
        new_line()


draw = Draw()
