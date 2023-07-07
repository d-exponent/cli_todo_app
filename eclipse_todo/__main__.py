import os
from typer import Typer, Option
from eclipse_todo.constants import SETTINGS_FILE
from eclipse_todo.helpers.settings import make_settings_file
from eclipse_todo.commands import create, read, delete
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers.utils import sum_true
from eclipse_todo.crud.db import Todos
from eclipse_todo.crud.csv import CSV


if not os.path.exists(SETTINGS_FILE):
    make_settings_file({"protocol": "csv", "database": {}})


app = Typer()

app.add_typer(create.app, name='create')
app.add_typer(read.app, name='read')
app.add_typer(delete.app, name='delete')


@app.command(help='Update a todo entry')
def update(
    db: bool = Option(
        help='Todo in the databse will be updated', default=False, show_default=False
    ),
    csv: bool = Option(
        help='Todo in  the csv file will be updated', default=False, show_default=False
    ),
    id: int = Option(prompt=True),
    todo: str = Option(prompt=True),
):
    """
    Only one flag can be provided betwwen the db and csv flags.
    Todo will not be updated if none or both flags are provided.
    """

    if sum_true(db, csv) != 1:
        print('Provide only one flag between (db) and (csv)')
        exit_app(1)

    db and Todos.update(id, todo)
    csv and CSV.update(id, todo)


app()
