import json
from eclipse_todo.constants import SETTINGS_FILE
from .prompt import prompt


def get_database_property(prop: str) -> str:
    db = get_settings()['database']
    return db.get(prop)


def get_settings() -> dict:
    with open(SETTINGS_FILE) as file:
        return json.load(file)


def make_settings_file(config: dict) -> None:
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(config, indent=2))


def update_settings(new_settings: dict) -> None:
    settings = get_settings()
    settings.update(new_settings)
    make_settings_file(settings)


def reset_db_password():
    new_password = prompt("password: ", False)
    db_settings = get_settings()['database']
    db_settings['password'] = new_password
    update_settings({'database': db_settings})


def set_database_credentials() -> dict:
    print("\nENTER YOUR DATABASE CREDENTIALS")
    db_settings = {}
    db_settings['name'] = prompt("database name: ", False, show_exit=True)
    db_settings['user'] = prompt("user: ", False)
    db_settings['password'] = prompt("password: ", False)
    db_settings['host'] = prompt("host: ", False)

    while True:
        try:
            port = prompt("port (Only numbers are allowed eg: 1234...): ", False)
            db_settings['port'] = int(port)
            break
        except ValueError:
            pass

    update_settings({"database": db_settings})
