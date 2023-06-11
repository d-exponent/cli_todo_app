if __name__ == '__main__':
    from eclipse_todo.commands import app
    from eclipse_todo.helpers.fs_todos import init_todos_file

    init_todos_file()
    app()
