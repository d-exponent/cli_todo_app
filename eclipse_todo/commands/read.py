from .typer_app import app
from typer import Option
from typing_extensions import Annotated
from typing import Optional

from eclipse_todo.classes.draw import draw
from eclipse_todo.helpers.utils import sum_true
from eclipse_todo.helpers.exceptions import exit_app


@app.command(help="View your current todo items.")
def read(
    db: Annotated[
        Optional[bool], Option(help="See all your todo items in the database")
    ] = False,
    fs: Annotated[
        Optional[bool], Option(help="See all your todo items in your local file system")
    ] = False,
):
    total_flags = sum_true(db, fs)

    if total_flags != 1:
        draw.db_todos()
        print('\n')
        draw.csv_todos()
        exit_app()

    if db:
        draw.db_todos()

    if fs:
        draw.csv_todos()
