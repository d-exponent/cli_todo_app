import json
from eclipse_todo.constants import SETTINGS_FILE_LOC


def current_protocol() -> str:
    return get_settings().get('protocol')


def get_settings() -> dict:
    with open(SETTINGS_FILE_LOC, 'r') as file:
        return json.load(file)


def update_settings(new_settings: dict) -> None:
    settings = get_settings().copy()
    settings.update(new_settings)

    with open(SETTINGS_FILE_LOC, 'w') as f:
        f.write(json.dumps(settings, indent=2))


def set_db() -> dict:
    print("\nENTER YOUR DATABASE CREDENTIALS")
    app_settings = get_settings()
    db_settings = app_settings['database']
    db_settings['name'] = input("database name: ")
    db_settings['username'] = input("username: ")
    db_settings['password'] = input("password: ")
    db_settings['host'] = input("host: ")

    while True:
        try:
            port = input("port (Only numbers are allowed eg: 1234): ")
            db_settings['port'] = int(port)
            break
        except ValueError:
            pass

    update_settings(app_settings)
    return db_settings
