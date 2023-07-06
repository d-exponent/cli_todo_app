import os
from typer import Typer

from eclipse_todo.constants import SETTINGS_FILE
from eclipse_todo.helpers.settings import make_settings_file


if not os.path.exists(SETTINGS_FILE):
    make_settings_file({"protocol": "csv", "database": {}})

if __name__ == '__main__':
    from eclipse_todo.commands import create, read

    app = Typer()
    app.add_typer(create.app, name='create')
    app.add_typer(read.app, name='read')

    app()
