from .typer_app import app
from eclipse_todo.helpers.draw import draw
from eclipse_todo.constants import CONFIG_DB_COMMAND
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.helpers import utils as u
from eclipse_todo.helpers import settings as st


SAVE_SUCCESS = "Your settings is saved successfully."


@app.command(help="Reset your database password")
def set_db_pass():
    """
    Set the password to your postgres instance
    """
    u.new_line()
    st.reset_db_password()
    u.new_line_then_print(SAVE_SUCCESS)
    exit_app()


@app.command(help="Set postgres database configuration")
def set_db_cred():
    """
    Set the postgres database configurations
    """
    st.set_database_credentials()
    u.new_line()
    draw.settings()
    print(SAVE_SUCCESS)
    exit_app()


# Allow the user to choose between postgres db or file system for todo operations
@app.command(help="Set preferred save protocol to preform CRUD on get")
def set_protocol(db: bool = False, csv: bool = False):
    total_true = u.sum_true(db, csv)
    if total_true == 0:
        u.new_line_then_print('ERROR: Provide either the --db or --csv flag')
        exit_app(1)

    if total_true == 2:
        u.new_line_then_print("Error: Provide one flag, either --csv or --db, not both")
        exit_app(1)

    settings = st.get_settings()
    protocol = settings['protocol']
    if csv:
        if protocol != 'csv':
            settings['protocol'] = 'csv'
            st.update_settings(settings)

    if db:
        db_settings = settings['database']
        if len(db_settings) != 5:
            print('Todos configuration is incomplete')
            u.new_line_then_print(CONFIG_DB_COMMAND)
            exit_app()

        if protocol != 'db':
            settings['protocol'] = 'db'
            st.update_settings(settings)

    print(SAVE_SUCCESS + " " + u.generate_save_loc_msg('csv' if csv else 'db'))
    exit_app()
