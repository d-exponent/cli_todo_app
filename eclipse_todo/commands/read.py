from typer import Option
from .typer_app import app

from eclipse_todo.helpers.utils import sum_true
from eclipse_todo.helpers.draw import draw
from eclipse_todo.helpers.utils import new_line


@app.command(help="View your current todo items.")
def view_todos(
    db: bool = Option(help="View todo items in the database", default=False),
    csv: bool = Option(help="View todo items in the csv file", default=False),
):
    if sum_true(db, csv) != 1:
        new_line()
        draw.db_todos()
        new_line()
        draw.csv_todos()
        new_line()
        return

    db and draw.db_todos()
    csv and draw.csv_todos()


@app.command(help='View the current settings')
def view_settings():
    draw.settings()
