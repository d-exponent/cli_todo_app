from .typer_app import app
from eclipse_todo.classes.draw import draw
from eclipse_todo.helpers import settings as s
from eclipse_todo.constants import CONFIG_DB_COMMAND
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers.utils import sum_true, generate_save_loc_msg

SAVE_SUCCESS = "Your settings is saved successfully."


@app.command(help="Set postgres database configuration")
def set_db_cred():
    """
    Sets the required postgres configurations and saves them in your local machine
    """
    s.set_database_credentials()
    print(SAVE_SUCCESS)
    draw.db_settings()


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

    settings = s.get_settings()
    protocol = settings['protocol']
    if fs:
        if protocol != 'fs':
            settings['protocol'] = 'fs'
            s.update_settings(settings)

    if db:
        db_settings = settings['database']
        if len(db_settings) != 5:
            msg = "Database configuration is incomplete\n" + CONFIG_DB_COMMAND
            print(msg)
            exit_app()

        if protocol != 'db':
            settings['protocol'] = 'db'
            s.update_settings(settings)
            draw.db_settings()

    print(SAVE_SUCCESS + " " + generate_save_loc_msg('fs' if fs else 'db'))
