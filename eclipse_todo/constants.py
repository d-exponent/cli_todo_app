from os import path, getcwd
from datetime import datetime


# FILES
main_dir = path.join(getcwd(), 'eclipse_todo', 'data')
SETTINGS_FILE = path.join(main_dir, "settings.json")
TODOS_FILE = path.join(main_dir, 'todos.csv')


YES_NO_EXIT_MSG = "Please enter y for YES, n for NO or EXIT to exit_app prompt"

# MESSAGES
YES_OPTIONS = ('y', 'yes')
NO_OPTIONS = ('n', 'no')

# COMMAND MESSAGES
CONFIG_DB_COMMAND = "RUN 'python.exe -m eclipse_todo set-db-cred' to reconfigure your database credentials"


# DATE TIME
YEAR_NOW = datetime.now().year
YEAR_IN_1OO = YEAR_NOW + 100
