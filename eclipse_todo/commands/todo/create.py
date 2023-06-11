from eclipse_todo.commands.typer_app import app
import pandas as pd

from psycopg2 import OperationalError, DatabaseError
from eclipse_todo.constants import TODOS_FILE, YEAR_NOW, YEAR_IN_1OO
from eclipse_todo.helpers.settings import get_current_protocol
from eclipse_todo.helpers.db import conn, close_connection
from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers.utils import (
    generate_save_loc_msg,
    validate_date_input,
)
from datetime import datetime


@app.command(help="create a new todo entry")
def create():
    now = datetime.now()
    protocol = get_current_protocol()
    msg = f"\nHey boss, your current save protocol is {protocol}. "

    print(msg + generate_save_loc_msg(protocol))
    print("It's time for a new todo. So exciting😀!!\n")

    content = prompt("What do you want to do?: ", False, show_exit=True)
    set_due_date = prompt("Do you want to set a due date [y/n]:  ", True)

    if set_due_date:
        try:
            day = validate_date_input(prompt("Enter day [1 to 31]: ", False), day=True)
            month = validate_date_input(
                prompt("Enter month [1 to 12]: ", False), month=True
            )
            year = validate_date_input(
                prompt(f"Enter year: [{YEAR_NOW} to {YEAR_IN_1OO}]: ", False),
                year=True,
            )
        except ValueError as e:
            if "invalid literal" in str(e):
                print("You entered a value that is not a number")
            else:
                print(e)
            exit_app(1)

        due_date = datetime(
            year=year if year else now.year,
            month=month if month else now.month,
            day=day if day else now.day,
        )

    if protocol == 'db':
        try:
            connection = conn()
            with connection.cursor() as cur:
                cur.execute(
                    'INSERT INTO todos (todo, due) VALUES (%s, %s);',
                    [content, due_date if set_due_date else None],
                )
                connection.commit()
                close_connection(connection)
        except OperationalError:
            close_connection(connection)
            print("OPERATIONAL ERROR: Please check your database credentials")
            exit_app(1)
        except DatabaseError:
            close_connection(connection)
            print("DATABASE ERROR: Something went wrong with database connection")
            exit_app(1)

    if protocol == 'fs':
        df = pd.DataFrame(
            {
                'todo': [content],
                'due': [str(due_date.date()) if set_due_date else None],
                'created_by': str(now).split('.')[0],
            }
        )

        df.to_csv(TODOS_FILE, mode='a', header=False, index=False)

    print("\n👍Todo was saved successfully")
