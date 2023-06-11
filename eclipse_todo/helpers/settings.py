import json
from eclipse_todo.constants import SETTINGS_FILE
from .prompt import prompt


def get_database_property(prop: str) -> str:
    db = get_settings()['database']
    return db.get(prop)


def get_settings() -> dict:
    with open(SETTINGS_FILE) as file:
        return json.load(file)


def update_settings(new_settings: dict) -> None:
    settings = get_settings().copy()
    settings.update(new_settings)
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(settings, indent=2))


def reset_db_password():
    db_settings = get_settings()['database']
    db_settings['password'] = prompt("password: ", return_bool=False)
    update_settings(db_settings)


def set_database_credentials(settings_file: str = SETTINGS_FILE) -> dict:
    print("\nENTER YOUR DATABASE CREDENTIALS")
    app_settings = get_settings()
    db_settings = app_settings['database']
    db_settings['name'] = prompt("database name: ", return_bool=False, show_exit=True)
    db_settings['user'] = prompt("user: ", return_bool=False)
    db_settings['password'] = prompt("password: ", return_bool=False)
    db_settings['host'] = prompt("host: ", return_bool=False)

    while True:
        try:
            port = prompt(
                "port (Only numbers are allowed eg: 1234): ", return_bool=False
            )
            db_settings['port'] = int(port)
            break
        except ValueError:
            pass

    update_settings(app_settings)
    return db_settings
