import os
from csv import writer, reader
from eclipse_todo.constants import TODOS_FILE


def init_todos_file():
    # ENSURE we have a todos file
    if not os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'x') as f:
            pass

    # --  ENSURE HEADERS ARE PROPERLY SET --
    headers = ['content', 'due', 'created']
    with open(TODOS_FILE, 'r') as f:
        file_headers = next(reader(f), None)

    if file_headers is None or file_headers != headers:
        with open(TODOS_FILE, 'w', newline='', encoding='UTF-8') as f:
            writer(f).writerow(headers)
