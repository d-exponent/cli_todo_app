import os
from eclipse_todo.constants import SETTINGS_FILE
from eclipse_todo.helpers.settings import make_settings_file


if not os.path.exists(SETTINGS_FILE):
    make_settings_file({"protocol": "fs", "database": {}})


if __name__ == '__main__':
    from eclipse_todo.commands import app

    app()
