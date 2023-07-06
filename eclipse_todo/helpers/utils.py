from datetime import datetime


def new_line():
    print("\n")


def new_line_then_print(msg: str = ""):
    new_line()
    print(msg)


def sum_true(*args):
    if args is None:
        return 0
    return sum([int(bool(i)) for i in args])


def generate_save_loc_msg(protocol):
    loc = 'csv file' if protocol == 'csv' else 'postgres database'
    return f"The application will save get to the {loc}."


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
