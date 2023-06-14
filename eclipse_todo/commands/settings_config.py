from .typer_app import app
from eclipse_todo.helpers.draw import draw
from eclipse_todo.constants import CONFIG_DB_COMMAND
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers import utils as u
from eclipse_todo.helpers import settings as st


SAVE_SUCCESS = "Your settings is saved successfully."


@app.command(help="Reset your database password")
def set_db_pass():
    u.new_line()
    st.reset_db_password()
    u.new_line_then_print(SAVE_SUCCESS)


@app.command(help="Set postgres database configuration")
def set_db_cred():
    """
    Sets the required postgres configurations and saves them in your local machine
    """
    st.set_database_credentials()
    u.new_line()
    draw.db_settings()
    u.new_line_then_print(SAVE_SUCCESS)


# Allow the user to choose between postgres db or file system for todo operations
@app.command(help="Set preferred save protocol to preform CRUD on todos")
def set_crud_proto(db: bool = False, fs: bool = False):
    total_true = u.sum_true(db, fs)
    if total_true == 0:
        u.new_line_then_print('ERROR: Provide either the --db or --fs flag')
        exit_app(1)

    if total_true == 2:
        u.new_line_then_print("Error: Provide one flag, either --fs or --db, not both")
        exit_app(1)

    settings = st.get_settings()
    protocol = settings['protocol']
    if fs:
        if protocol != 'fs':
            settings['protocol'] = 'fs'
            st.update_settings(settings)

    if db:
        db_settings = settings['database']
        if len(db_settings) != 5:
            print('Database configuration is incomplete')
            u.new_line_then_print(CONFIG_DB_COMMAND)
            exit_app()

        if protocol != 'db':
            settings['protocol'] = 'db'
            st.update_settings(settings)

    print(SAVE_SUCCESS + " " + u.generate_save_loc_msg('fs' if fs else 'db'))
