import csv
from rich import box
from rich.table import Table
from rich.console import Console
from dataclasses import dataclass

from eclipse_todo.constants import CREATE_TODO, CONFIG_DB_COMMAND, TODOS
from eclipse_todo.helpers.utils import new_line_then_print, new_line
from eclipse_todo.crud.database import Todos
from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.decorators import key_error_handler, file_not_found_handler


TODOS_TABLE = 'todos'
SETTINGS_TABLE = 'settings'


# UTILITY FUNTION
def set_columns(table_name: str, config: dict) -> Table:
    allowed = ('todos', 'settings')
    assert table_name in allowed, 'table can either be "todos" or "settings"'

    table = Table(**config)

    if table_name == 'todos':
        table.add_column("Id")
        table.add_column("Todos", style='cyan', no_wrap=False)
        table.add_column("Due", style="red")
        table.add_column("Created_at", justify="left", style="green")

    if table_name == 'settings':
        table.add_column('Type')
        table.add_column("Name")
        table.add_column("User")
        table.add_column("Password")
        table.add_column("Host")
        table.add_column("Port")

    return table


@dataclass
class Draw:
    console: Console = Console()

    @file_not_found_handler
    def csv_todos(self) -> None:
        table = set_columns(TODOS_TABLE, {'title': "CSV Todos"})

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

    @key_error_handler
    @file_not_found_handler
    def settings(self) -> None:
        table = set_columns(
            SETTINGS_TABLE,
            {'title': "Database Settings", 'box': box.HORIZONTALS},
        )

        settings = get_settings()
        db_type = settings['type']

        table.add_row(
            db_type,
            settings.get('database'),
            settings.get('user'),
            settings.get('password'),
            settings.get('host'),
            str(settings.get('port')) if db_type == 'postgres' else 'None',
        )

        self.console.print(table)
        print(CONFIG_DB_COMMAND)
        new_line()


draw = Draw()
