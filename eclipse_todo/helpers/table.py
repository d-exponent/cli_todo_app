from rich import table
from eclipse_todo.wrappers import console


def draw_table(data: dict, msg: str = "") -> None:
    print(msg)
    data_iter = data.items()
    headers = (setting[0] for setting in data_iter)
    row = (setting[1] for setting in data_iter)

    console.init_table(table.Table(*headers))
    console.add_table_row(row)
    console.print_table()
