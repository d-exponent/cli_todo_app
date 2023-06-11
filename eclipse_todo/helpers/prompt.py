from eclipse_todo.constants import YES_OPTIONS, NO_OPTIONS, YES_NO_EXIT_MSG
from eclipse_todo.helpers.exceptions import exit_app


def prompt(msg: str, return_bool: bool = True, show_exit=False):
    show_exit and print('Enter EXIT at any prompt to quit the application')
    user_input = input(msg).lower()

    if 'exit' in user_input:
        exit_app()

    if not return_bool:
        return user_input

    # return_bool argument is True here
    if user_input not in NO_OPTIONS and user_input not in YES_OPTIONS:
        print('\n' + YES_NO_EXIT_MSG)
        return prompt(msg, True, show_exit=False)

    return user_input in YES_OPTIONS
