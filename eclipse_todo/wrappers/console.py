from dataclasses import dataclass
from rich.console import Console
from rich.table import Table


@dataclass
class MyConsole:
    console: Console = Console()
    table: Table = None

    def init_table(self, table: Table):
        self.table = table

    def add_table_row(self, rows: tuple | list):
        serialized_rows = []
        for row in rows:
            if not isinstance(row, str):
                serialized_rows.append(str(row))
            else:
                serialized_rows.append(row)

        self.table.add_row(*serialized_rows)

    def print_table(self):
        self.console.print(self.table)
        self.table = None


console = MyConsole()
