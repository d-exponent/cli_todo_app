from typer import Exit, Argument
from .typer_app import app
from eclipse_todo.constants import YES_NO_EXIT_MSG, YES_OPTIONS, NO_OPTIONS
from eclipse_todo.helpers.settings import get_settings, update_settings, set_db
from eclipse_todo.helpers.table import draw_table
from eclipse_todo.helpers.exceptions import check_exit_abort


SUCCESSFULL_SAVE_MSG = "Your settings is saved successfully"


# Allow the usser to choose between postgres db or file system for todo operations
@app.command()
def config(protocol: str = Argument(help="The preferred save protocol to preform CRUD on todos")):
    """
    Configure the save protocol to be used.\n
    The protocol determines where your todo will be read from and written to\n
    - fs: Perform CRUD to todo in your file system\n
    - db: Perform CRUD to todo in a postgres database instance. You are responsible for maintaining your database\n
    **The postgres instance url parameters will be provided by you. All settings are stored on your local machine **
    RUN eclipse_todo show_db_params to see required postgres paramaters
    """

    settings = get_settings()
    if protocol != settings['protocol']:
        settings["protocol"] = protocol
        update_settings(settings)

    if protocol == 'fs':
        print(SUCCESSFULL_SAVE_MSG + " Your todos will be saved to the files system")
        raise Exit()

    # Ask for db config values
    if protocol == 'db':
        db_settings = settings['database']
        has_db_config = len(db_settings) > 0

        if has_db_config is False:
            new_settings = set_db()
            draw_table(new_settings, "Your new database settings below")
            raise Exit()

        # ASK TO UPDATE DB CONFIGURATION ?
        draw_table(db_settings, '\nThe Current database settings')

        print('\n')
        while True:
            update_db_config = input("Update your databse settings? [y/n]: ").lower()
            check_exit_abort(update_db_config)

            if update_db_config in NO_OPTIONS:
                print('\n')
                break

            if update_db_config not in YES_OPTIONS:
                print("\n" + YES_NO_EXIT_MSG)
                continue

            # update_db_config in YES_OPTIONS:
            new_settings = set_db()
            draw_table(new_settings, "\nYour new database settings below")
            
            print('\n')
            while True:
                satisfied = input("Satisfied with settings? [y/n] ")
                check_exit_abort(satisfied)

                if satisfied in YES_OPTIONS:
                    print(SUCCESSFULL_SAVE_MSG)
                    raise Exit()

                if satisfied in NO_OPTIONS:
                    print('\n')
                    break

                print("\n" + YES_NO_EXIT_MSG)

        print(SUCCESSFULL_SAVE_MSG)
