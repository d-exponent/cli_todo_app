import os
from csv import writer, reader
from eclipse_todo.constants import TODOS_FILE


def init_todos_file():
    try:
        with open(TODOS_FILE, 'x') as f:
            pass
    except FileExistsError:
        pass

    # --  ENSURE HEADERS ARE PROPERLY SET --
    headers = ['todo', 'due', 'created_by']
    with open(TODOS_FILE, 'r') as f:
        file_headers = next(reader(f), None)

    if file_headers is None or file_headers != headers:
        with open(TODOS_FILE, 'w', newline='', encoding='UTF-8') as f:
            writer(f).writerow(headers)
