from datetime import datetime


def new_line():
    print("\n")


def new_line_then_print(msg: str = ""):
    new_line()
    print(msg)


def sum_true(*args):
    total = 0
    if args is None:
        return total

    for arg in args:
        total += int(bool(arg))
    return total


def generate_save_loc_msg(protocol):
    loc = 'file system' if protocol == 'fs' else 'postgres database'
    return f"The application will save todos to your {loc}."


def validate_date_input(
    input: str, day: bool = False, month: bool = False, year: bool = False
):
    assert sum_true(day, month, year) == 1, 'Must provide only one flag'
    if input == "":
        return input

    input_int = int(input)
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
