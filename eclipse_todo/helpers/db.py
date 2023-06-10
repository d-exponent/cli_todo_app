from psycopg2 import connect, OperationalError
from eclipse_todo.constants import CONFIG_DB_COMMAND
from typer import Exit

from .settings import get_settings, set_db
from .prompt import prompt


def conn():
    try:
        db_cred = get_settings()['database']
        if len(db_cred.items()) == 5:
            return connect(
                database=db_cred.get('name'),
                user=db_cred.get('user'),
                password=db_cred.get('password'),
                host=db_cred.get('host'),
                port=db_cred.get('port'),
            )

        print("Your database credentials is incomplete")
        prompt_msg = "Would you like to reset your database credentials? [y/n] "
        reset = prompt(prompt_msg, True)

        if reset is False:
            print("Aborting connection to database")
            raise Exit()

        set_db()
        return conn()
    except OperationalError:
        err_msg = "ERROR: connecting to the databse failed. Common reason is bad  db credentials\n"
        print(err_msg + CONFIG_DB_COMMAND)
        raise Exit()
