from .typer_app import app
from eclipse_todo.constants import CONFIG_DB_COMMAND
from eclipse_todo.helpers.settings import (
    get_settings,
    update_settings,
    set_database_credentials,
)
from eclipse_todo.helpers.table import draw_table
from eclipse_todo.helpers.utils import sum_true
from eclipse_todo.helpers.exceptions import exit_app

SAVE_SUCCESS = "Your settings is saved successfully."


@app.command(help="Set postgres database configuration")
def set_db_cred():
    """
    Sets the required postgres configurations and saves them in your local machine
    """
    new_credentials = set_database_credentials()
    print(SAVE_SUCCESS)
    draw_table(new_credentials, "\nYour new database settings below")


# Allow the user to choose between postgres db or file system for todo operations
@app.command(help="Set preferred save protocol to preform CRUD on todos")
def set_crud_proto(db: bool = False, fs: bool = False):
    total_true = sum_true(db, fs)
    if total_true == 0:
        msg = '\nERROR: Provide either the --db or --fs flag'
        print(msg)
        exit_app(1)

    if total_true == 2:
        msg = '\nError: You can only provide one flag, either --fs or --db, not both'
        print(msg)
        exit_app(1)

    settings = get_settings()
    protocol = settings['protocol']
    if fs:
        if protocol != 'fs':
            settings['protocol'] = 'fs'
            update_settings(settings)

    if db:
        db_settings = settings['database']
        if len(db_settings) != 5:
            msg = "Database configuration is incomplete\n" + CONFIG_DB_COMMAND
            print(msg)
            exit_app()

        if protocol != 'db':
            settings['protocol'] = 'db'
            update_settings(settings)
            draw_table(db_settings, 'Your Database configurations')

    loc = 'file system' if fs else 'postgres database'
    print(SAVE_SUCCESS + f" Application will save todos to your {loc}")
