from os import path, getcwd

SETTINGS_FILE_LOC = path.join(getcwd(), "eclipse_todo", "settings.json")
YES_NO_EXIT_MSG = "Please enter y for YES, n for NO or EXIT to exit prompt"
YES_OPTIONS = ('y', 'yes')
NO_OPTIONS = ('n', 'no')

# CONFIG MESSAGES
CONFIG_DB_COMMAND = (
    "RUN 'python.exe -m eclipse_todo config-db' to reconfigure your databse credentials"
)
