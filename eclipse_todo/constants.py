from os import path, getcwd
from datetime import datetime

# PROMPT
YES_NO_EXIT_MSG = "Please enter y for YES, n for NO or EXIT to exit_app prompt"

# COMMAND MESSAGES
CONFIG_DB_COMMAND = "RUN 'python.exe -m eclipse_todo set-db-cred' to configure your database credentials"
CREATE_TODO = "RUN 'python.exe -m eclipse_todo create' to add a new todo"

# ERRORS
PG_OPERATIONAL_ERR = (
    "🛑 OPERATIONAL ERROR: Check your database credentials\n" + CONFIG_DB_COMMAND
)
PG_DATABASE_ERR = (
    "🛑 DATABASE ERROR: Something went wrong with the database\n" + CONFIG_DB_COMMAND
)

# FILES
main_dir = path.join(getcwd(), 'eclipse_todo', 'assets')
SETTINGS_FILE = path.join(main_dir, "settings.json")
TODOS = path.join(main_dir, 'todos.csv')


# OPTIONS
YES_OPTIONS = ('y', 'yes')
NO_OPTIONS = ('n', 'no')


# DATE TIME
YEAR_NOW = datetime.now().year
YEAR_IN_1OO = YEAR_NOW + 100
