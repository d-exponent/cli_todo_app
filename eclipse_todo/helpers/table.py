from rich.table import Table


def set_columns(table_name: str, config: dict) -> Table:
    allowed = ('todos', 'settings')
    assert table_name in allowed, 'table can either be "todos" or "settings"'

    table = Table(**config)

    if table_name == 'todos':
        table.add_column("Index")
        table.add_column("Todo", style='cyan', no_wrap=False)
        table.add_column("Due", style="red")
        table.add_column("Created_at", justify="left", style="green")

    if table_name == 'settings':
        table.add_column("Name")
        table.add_column("User")
        table.add_column("Password")
        table.add_column("Host")
        table.add_column("Port")

    return table
