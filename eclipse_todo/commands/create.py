from typer import Option, Typer
from datetime import datetime

from eclipse_todo.constants import YEAR_IN_1OO, YEAR_NOW
from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.crud.todos import Todos
from eclipse_todo.crud.csv import TodoEntry, CSV
from eclipse_todo.helpers.utils import validate_date_input, new_line_then_print
from eclipse_todo.helpers.draw import draw


NOW = datetime.now()
SHOW_TABLE_HELP = 'View table after new todo entry'
SAVED_SUCCESS_MSG = 'The todo was saved successfully'


def get_user_todo():
    new_line_then_print("It's time for a new todo. So exciting😀!!")
    todo = prompt("What do you want to do?: ", False, show_exit=True)
    set_due_date = prompt("Do you want to set a due date [y/n]:  ", True)

    due_date, year, month, day = [None for _ in range(4)]

    if set_due_date:
        day_prompt = "Enter day [1 to 31]: "
        month_prompt = "Enter month [1 to 12]: "
        year_prompt = f"Enter year: [{YEAR_NOW} to {YEAR_IN_1OO}]: "

        try:
            day = validate_date_input(prompt(day_prompt, False), day=True)
            month = validate_date_input(prompt(month_prompt, False), month=True)
            year = validate_date_input(prompt(year_prompt, False), year=True)
        except ValueError as e:
            if "invalid literal" in str(e):
                print("You entered a value that is not a number")
            else:
                print(e)
            exit_app(1)

        due_date = datetime(
            year=year if year else NOW.year,
            month=month if month else NOW.month,
            day=day if day else NOW.day,
        )

    return TodoEntry(todo, due_date)


app = Typer(help='Create a new todo entry in your local machine or postgres instance')


@app.command(help='Create a todo entry in your database table')
def db(show_table: bool = Option(help=SHOW_TABLE_HELP, default=False)):
    new_todo = get_user_todo()
    Todos.create([new_todo.todo, new_todo.due])
    new_line_then_print(SAVED_SUCCESS_MSG)
    show_table and draw.db_todos(sort=-1)
    exit_app()


@app.command(help='Create a todos entry in your local machine')
def csv(show_table: bool = Option(help=SHOW_TABLE_HELP, default=False)):
    CSV.create(new_todo=get_user_todo())
    new_line_then_print(SAVED_SUCCESS_MSG)
    show_table and draw.csv_todos()
    exit_app()
