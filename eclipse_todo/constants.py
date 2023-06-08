from os import path, getcwd

SETTINGS_FILE_LOC = path.join(getcwd(), "eclipse_todo", "settings.json")
YES_NO_EXIT_MSG = "Please enter y for YES, n for NO or EXIT to exit prompt"
YES_OPTIONS = ('y', 'YES')
NO_OPTIONS = ('n', 'no')
