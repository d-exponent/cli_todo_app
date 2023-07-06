from typer import Option, Typer

from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.helpers.draw import draw
from eclipse_todo.helpers.exceptions import exit_app
from eclipse_todo.crud.todos import Todos

db_todos_help_msgs = {
    'recent': 'View from the most recently added todos',
    'limit': 'The total number of rows per page',
}

app = Typer(help='View todos and settings')


@app.command(help='View todos saved in your postgres database')
def db(
    recent: bool = Option(help=db_todos_help_msgs['recent'], default=False),
    limit: int = Option(help=db_todos_help_msgs['limit'], default=25, min=5, max=30),
):
    total_todos = Todos.count()
    sort = -1 if recent else 1
    skip = 0
    count = total_todos if total_todos < limit else limit

    print(f'Total todos: {total_todos}')

    while True:
        draw.db_todos(skip, sort=sort, limit=limit, alert=False)
        remaining = total_todos - count

        if remaining <= 0:
            break

        print(f'{remaining if remaining > 0 else 0} todos left')

        if not prompt('See more? [y/n]: ', True, show_exit=False):
            break

        next_count = count if count < limit else limit
        count += next_count
        skip += next_count


@app.command(help="View todos saved your local machine csv file.")
def csv():
    draw.csv_todos()  # TODO: Paginate csv
    exit_app()


@app.command(help='View the current application settings')
def settings():
    draw.settings()
    exit_app()
