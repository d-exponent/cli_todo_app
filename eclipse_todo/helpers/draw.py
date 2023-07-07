import csv
from rich import box
from rich.console import Console
from dataclasses import dataclass

from eclipse_todo.constants import CREATE_TODO, CONFIG_DB_COMMAND, TODOS
from eclipse_todo.helpers.utils import new_line_then_print, new_line
from eclipse_todo.crud.db import Todos
from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.table import set_columns


TODOS_TABLE = 'todos'
SETTINGS_TABLE = 'settings'


@dataclass
class Draw:
    console: Console = Console()

    def csv_todos(self) -> None:
        table = set_columns(TODOS_TABLE, {'title': "CSV Todos"})
        try:
            with open(TODOS, 'r') as data:
                for i, row in enumerate(csv.reader(data)):
                    if i == 0:  # avoid the headers
                        # This will be adjusted in CSV crud class by -1 to correct ...
                        # ... the index the user sees to the actual todo index
                        continue
                    else:
                        row.insert(0, str(i))
                        table.add_row(*row)

                new_line()
                self.console.print(table)
                new_line()
        except FileNotFoundError:
            new_line_then_print("Csv get is currently empty.")
            new_line_then_print(CREATE_TODO)
            new_line()

    def db_todos(
        self,
        skip: int = 0,
        limit: int = 25,
        sort: int = 1,
        alert: bool = True,
        reader: Todos = Todos,
    ) -> None:
        table = set_columns(TODOS_TABLE, {'title': "Databse Todos"})

        rows = reader.get_many(sort=sort, skip=skip, limit=limit)
        if len(rows) == 0:
            alert and new_line_then_print("Todos list is currently empty.")
            alert and new_line_then_print(CREATE_TODO)
        else:
            for row in rows:
                new_row = (str(row[0]), row[1], str(row[2]), str(row[3]).split('.')[0])
                table.add_row(*new_row)

        new_line()
        self.console.print(table)
        new_line()

    def settings(self) -> None:
        table = set_columns(
            SETTINGS_TABLE,
            {'title': "Postgres Connection Settings.", 'box': box.HORIZONTALS},
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
