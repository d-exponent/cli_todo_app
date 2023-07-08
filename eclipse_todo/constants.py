from os import path, getcwd
from datetime import datetime


# COMMAND MESSAGES
CONFIG_DB_COMMAND = (
    " RUN 'python.exe -m eclipse_todo init --help to configure database settings' "
)

CREATE_TODO = "RUN 'python.exe -m eclipse_todo create' to add a new todo"


# FILES
main_dir = path.join(getcwd(), 'eclipse_todo', 'assets')
SETTINGS_FILE = path.join(main_dir, "settings.json")
TODOS = path.join(main_dir, 'todos.csv')


# DATE TIME
YEAR_NOW = datetime.now().year
YEAR_IN_1OO = YEAR_NOW + 100
