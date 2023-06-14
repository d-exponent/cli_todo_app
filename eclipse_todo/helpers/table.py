from rich.table import Table


def create_set_columns(table_name: str, config: dict) -> Table:
    will_accept = ('todos', 'settings')
    assert table_name in will_accept, 'table can either be "todos" or "settings"'

    table = Table(**config)
    if table_name == 'todos':
        table.add_column("Index", justify='left')
        table.add_column("Todo", justify='left', style='cyan', no_wrap=False)
        table.add_column("Due", justify="left", style="red")
        table.add_column("Created_at", justify="left", style="green")

    if table_name == 'settings':
        table.add_column("Name")
        table.add_column("User")
        table.add_column("Password")
        table.add_column("Host")
        table.add_column("Port")

    return table
