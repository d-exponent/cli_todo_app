from typer import Option
from .typer_app import app

from eclipse_todo.helpers.utils import sum_true
from eclipse_todo.helpers.draw import draw
from eclipse_todo.helpers.utils import new_line


@app.command(help="View your current todo items.")
def read(
    db: bool = Option(help="View todo items in the database", default=False),
    fs: bool = Option(help="View todo items in your local file system", default=False),
):
    if sum_true(db, fs) != 1:
        draw.db_todos()
        new_line()
        draw.csv_todos()
        return

    db and draw.db_todos()
    fs and draw.csv_todos()
