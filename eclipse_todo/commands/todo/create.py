import os
import csv
import pandas as pd
from datetime import datetime
from psycopg2 import OperationalError, DatabaseError

from eclipse_todo.helpers.db import conn
from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.commands.typer_app import app
from eclipse_todo.classes.draw import draw
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers.settings import get_current_protocol
from eclipse_todo import constants as c
from eclipse_todo.helpers.utils import generate_save_loc_msg, validate_date_input


@app.command(help="create a new todo entry")
def create():
    now, protocol = (datetime.now(), get_current_protocol())
    msg = f"\nHey boss, your current save protocol is {protocol}. "

    print(msg + generate_save_loc_msg(protocol))
    print("It's time for a new todo. So exciting😀!!\n")

    content = prompt("What do you want to do?: ", False, show_exit=True)
    set_due_date = prompt("Do you want to set a due date [y/n]:  ", True)

    if set_due_date:
        day_prompt = "Enter day [1 to 31]: "
        month_prompt = "Enter month [1 to 12]: "
        year_prompt = f"Enter year: [{c.YEAR_NOW} to {c.YEAR_IN_1OO}]: "

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
            year=year if year else now.year,
            month=month if month else now.month,
            day=day if day else now.day,
        )

    if protocol == 'db':
        try:
            with conn() as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        'INSERT INTO todos (todo, due) VALUES (%s, %s);',
                        [content, due_date if set_due_date else None],
                    )
                    connection.commit()
            draw.db_todos()
        except OperationalError:
            print(c.PG_OPERATIONAL_ERR)
            exit_app(1)
        except DatabaseError:
            print(c.PG_DATABASE_ERR)
            exit_app(1)

    if protocol == 'fs':
        is_todos_exist = os.path.exists(c.TODOS_FILE)
        new_todo = {
            'todo': [content],
            'due': [str(due_date.date()) if set_due_date else None],
            'created_at': str(now).split('.')[0],
        }

        # Create the csv todos file if it doesn't exist
        if not is_todos_exist:
            with open(c.TODOS_FILE, 'x'):
                pass

        # Retrieve the csv file headers
        with open(c.TODOS_FILE, 'r') as f:
            headers = next(csv.reader(f), None)
            has_headers = bool(headers)

        df = pd.DataFrame(new_todo)
        df.to_csv(c.TODOS_FILE, mode='a', header=not has_headers, index=True)
        draw.csv_todos()

    print("\n👍Todo was saved successfully")
