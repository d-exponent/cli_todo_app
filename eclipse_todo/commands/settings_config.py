from .typer_app import app
from eclipse_todo.constants import CONFIG_DB_COMMAND
from eclipse_todo.helpers.settings import get_settings, update_settings, set_db
from eclipse_todo.helpers.table import draw_table
from eclipse_todo.helpers.utils import sum_objects
from eclipse_todo.helpers.exceptions import exit


SAVE_SUCCESS = "Your settings is saved successfully."


@app.command(help="Set postgres database configuration")
def set_database():
    """
    Sets the required postgres configurations and saves them in your local machine
    """
    new_settings = set_db()
    print(SAVE_SUCCESS)
    draw_table(new_settings, "\nYour new database settings below")


# Allow the usser to choose between postgres db or file system for todo operations
@app.command(help="Set preferred save protocol to preform CRUD on todos")
def set_protocol(db: bool = False, fs: bool = False):
    if sum_objects(db, fs) != 1:
        print('\nERROR: You can only provide one (1) between db and fs')
        exit(1)

    settings = get_settings()
    protocol = settings['protocol']
    if fs:
        if protocol != 'fs':
            settings['protocol'] = 'fs'
            update_settings(settings)

    if db:
        if protocol != 'db':
            settings['protocol'] = 'db'
            update_settings(settings)

        db_settings = settings['database']
        if len(db_settings) != 5:
            print("Database configuration is incomplete\n" + CONFIG_DB_COMMAND)
            exit()
        else:
            draw_table(db_settings, 'Your Database configurations')

    loc = 'file system' if fs else 'postgress database'
    print(SAVE_SUCCESS + f" Application will save todos to your {loc}")
