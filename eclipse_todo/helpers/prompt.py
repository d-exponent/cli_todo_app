from eclipse_todo.helpers.exit import exit_app

YES_NO_EXIT_MSG = "Please enter y for YES, n for NO or EXIT to exit the prompt"
YES_OPTIONS = ('y', 'yes')


def prompt(msg: str, return_bool: bool = True, show_exit=False):
    show_exit and print('Enter EXIT at any prompt to quit the application')
    user_input = input(msg).lower()

    if 'exit' in user_input:
        exit_app()

    if not return_bool:
        return user_input

    # return_bool argument is True here
    if user_input not in ('n', 'no') and user_input not in ('y', 'yes'):
        print('\n' + YES_NO_EXIT_MSG)
        return prompt(msg, True, show_exit=False)

    return user_input in YES_OPTIONS
