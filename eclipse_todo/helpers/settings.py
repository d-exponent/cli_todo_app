import json
from eclipse_todo.constants import SETTINGS_FILE
from .prompt import prompt


def get_settings() -> dict:
    with open(SETTINGS_FILE) as file:
        return json.load(file)


def make_settings_file(config: dict) -> None:
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(config, indent=2))


def set_database_credentials(use_port=True) -> dict:
    db_settings = {
        'database': prompt("Database: ", False, show_exit=True),
        'user': prompt("User: ", False),
        'password': prompt("Password: ", False),
        'host': prompt("Host: ", False),
        'table': prompt('Table Name: ', False),
    }

    if use_port:
        while True:
            try:
                port = prompt("Port (Only numbers eg: 1234...): ", False)
                db_settings['port'] = int(port)
                break
            except ValueError:
                pass

    return db_settings
