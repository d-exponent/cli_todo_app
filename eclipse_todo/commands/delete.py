from typer import Option, Typer

from eclipse_todo.crud.db import Todos
from eclipse_todo.crud.csv import CSV
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers.utils import new_line


DELETE_SUCCESS_MSG = "Todo was deleted successfully"
csv_help = 'The id of the todo to be deleted. Defaults to the most recent todo entry'

app = Typer(help='Delete todos from CSV and postgres database instance')


@app.command(help='Delete todo')
def csv(id: int = Option(help=csv_help, default=0, show_default=False)):
    CSV.delete(id)
    print(DELETE_SUCCESS_MSG)
    new_line()
    exit_app()


@app.command(help='Delete todo entry by id')
def db(id: int = Option(help='The id of the todo to be deleted.')):
    Todos.delete(id)
    print(DELETE_SUCCESS_MSG)
    new_line()
    exit_app()
