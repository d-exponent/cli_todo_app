from datetime import datetime

from eclipse_todo.constants import YEAR_IN_1OO, YEAR_NOW
from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.helpers.exit import exit_app
from eclipse_todo.crud.csv import TodoEntry
from eclipse_todo.helpers.utils import sum_true


NOW = datetime.now()


def validate_date_input(
    entry: str, day: bool = False, month: bool = False, year: bool = False
):
    assert sum_true(day, month, year) == 1, 'Must provide only one flag'
    if entry == "":
        return entry

    input_int = int(entry)
    if day and input_int not in range(1, 32):
        raise ValueError('A day must be between 1 to 31')

    if month and input_int not in range(1, 13):
        raise ValueError("A month must be between 1 and 12")

    year_now = datetime.now().year
    year_in_100 = year_now + 100
    if year and input_int not in range(year_now, year_in_100):
        msg = f"A year must be between {year_now} and {year_in_100}"
        raise ValueError(msg)

    return input_int


def get_user_todo():
    todo = prompt("New todo: ", False, show_exit=True)
    set_due_date = prompt("Set a due date [y/n]:  ", True)

    due_date, year, month, day = [None for _ in range(4)]

    if set_due_date:
        day_prompt = "Day [1 to 31]: "
        month_prompt = "Month [1 to 12]: "
        year_prompt = f"Year: [{YEAR_NOW} to {YEAR_IN_1OO}]: "

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
