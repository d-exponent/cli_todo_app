from typing import Callable
import psycopg2 as postgres
import mysql.connector as mysql
from mysql.connector import errorcode

from eclipse_todo.helpers.exit import exit_app
from eclipse_todo.constants import CONFIG_DB_COMMAND, CREATE_TODO


# UTILITY FUNTION
def print_exit(msg: str):
    print(msg)
    exit_app(1)


# DECORATOR TO HANDLE DATABASE ERRORS
def guard_conn(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except postgres.OperationalError as err:
            print_exit(err)
        except postgres.DatabaseError as err:
            print_exit(err)
        except mysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print_exit("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print_exit("Database does not exist")
            else:
                print_exit(err)

    return wrapper


def file_not_found_handler(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as error:
            errorMsg = str(error)
            if 'settings.json' in errorMsg:
                print_exit(f'😥OOPS No Settings file\n{CONFIG_DB_COMMAND}')

            if 'todos.csv' in errorMsg:
                print_exit(f'OOPS! No csv Todos.\n{CREATE_TODO}')

            print_exit(errorMsg)

    return wrapper


@file_not_found_handler
def key_error_handler(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as err:
            all_settings_keys = [
                'database',
                'user',
                'password',
                'host',
                'table',
                'port',
                'type',
            ]
            if str(err) in all_settings_keys:
                print_exit(f'{err} is not set in settings file')
                print_exit(CONFIG_DB_COMMAND)
            else:  # developer error
                print_exit('Silly me 😪. No such key as => ' + str(err))

    return wrapper
