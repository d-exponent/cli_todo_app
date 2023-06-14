import os
import csv
import pandas as pd
from datetime import datetime
from .typer_app import app

from eclipse_todo.constants import TODOS_FILE, YEAR_IN_1OO, YEAR_NOW
from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers.database import add_db_todo
from eclipse_todo.helpers.settings import get_settings
from eclipse_todo.helpers.utils import generate_save_loc_msg, validate_date_input


@app.command(help="create a new todo entry")
def create():
    now, protocol = (datetime.now(), get_settings()['protocol'])
    msg = f"\nHey boss, your current save protocol is {protocol}. "

    print(msg + generate_save_loc_msg(protocol))
    print("It's time for a new todo. So exciting😀!!\n")

    content = prompt("What do you want to do?: ", False, show_exit=True)
    set_due_date = prompt("Do you want to set a due date [y/n]:  ", True)

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
            year=year if year else now.year,
            month=month if month else now.month,
            day=day if day else now.day,
        )

    if protocol == 'db':
        params = [content, due_date if set_due_date else None]
        add_db_todo(params)

    if protocol == 'fs':
        is_todos_exist = os.path.exists(TODOS_FILE)
        new_todo = {
            'todo': [content],
            'due': [str(due_date.date()) if set_due_date else None],
            'created_at': str(now).split('.')[0],
        }

        # Create the csv todos file if it doesn't exist
        if not is_todos_exist:
            with open(TODOS_FILE, 'x'):
                pass

        # Retrieve the csv file headers
        with open(TODOS_FILE, 'r') as f:
            headers = next(csv.reader(f), None)
            has_headers = bool(headers)

        df = pd.DataFrame(new_todo)
        df.to_csv(TODOS_FILE, mode='a', header=not has_headers, index=True)

    print("\n👍Todo was saved successfully")
