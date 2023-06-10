from eclipse_todo.constants import YES_OPTIONS, NO_OPTIONS, YES_NO_EXIT_MSG
from typer import Exit


def prompt(msg: str, bool: bool = True, show_exit=False):
    show_exit and print('Enter EXIT to quit the prompt')
    user_input = input(msg).lower()

    if 'exit' in user_input:
        raise Exit()

    if not bool:
        return user_input

    # bool argument is True here
    if user_input not in NO_OPTIONS and user_input not in YES_OPTIONS:
        print('\n' + YES_NO_EXIT_MSG)
        return prompt(msg, True, show_exit=False)

    return user_input in YES_OPTIONS
