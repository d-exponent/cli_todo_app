from typer import Typer, Option
from eclipse_todo import read
from eclipse_todo.helpers import settings as st
from eclipse_todo.helpers.exit import exit_app
from eclipse_todo.helpers.utils import sum_true
from eclipse_todo.helpers.prompt import prompt
from eclipse_todo.helpers.commands.create import get_user_todo
from eclipse_todo.helpers.commands.init import create_table
from eclipse_todo.crud.database import Todos
from eclipse_todo.crud.csv import CSV
from eclipse_todo.helpers.draw import draw


CHOOSE_BETWEEN_CSV_DB_MSG = 'Provide one flag between (db) and (csv)'


app = Typer()
app.add_typer(read.app, name='read')


@app.command(help='Initialize application with postgres or mysql database credentials')
def init(
    pg: bool = Option(help='use postgres database', default=False),
    mysql: bool = Option(help='use mysql database', default=False),
):
    if sum_true(pg, mysql) != 1:
        print("Provide only --pg OR --mysql flag")
        exit_app(1)

    print('Enter database credentials')
    db_cred = st.set_database_credentials(use_port=pg)
    db_cred['type'] = 'postgres' if pg else 'mysql'

    table = db_cred['table']
    st.make_settings_file(config=db_cred)
    print('Database credentials saved successfully. 👍')

    create_table(table=table, pg=pg, mysql=mysql)
    print(f'{table} was created successfully')


@app.command(help='Create a todo')
def create(
    db: bool = Option(help='Create todo to db', default=False),
    csv: bool = Option(help='Create todo to local csv file', default=False),
    show_table: bool = Option(help='Show table after save', default=False),
):
    if sum_true(db, csv) != 1:
        print('Enter eiter the --db flag or the --csv flag')
        exit_app()

    new_todo = get_user_todo()
    db and Todos.create(new_todo)
    csv and CSV.create(new_todo)

    print("Todo was saved successfully 👌")

    if show_table:
        db and draw.db_todos(sort=-1, limit=10)
        csv and draw.csv_todos()


@app.command(help='Update a todo entry')
def update(
    db: bool = Option(
        help='Todo in the databse will be updated', default=False, show_default=False
    ),
    csv: bool = Option(
        help='Todo in  the csv file will be updated', default=False, show_default=False
    ),
    id: int = Option(prompt=True),
    todo: str = Option(prompt=True),
):
    """
    Only one flag can be provided betwwen the db and csv flags.
    Todo will not be updated if none or both flags are provided.
    """

    if sum_true(db, csv) != 1:
        print(CHOOSE_BETWEEN_CSV_DB_MSG)
        exit_app(1)

    db and Todos.update(id, todo)
    csv and CSV.update(id, todo)
    print("Update was successfull 😎")


@app.command(help='Delete a todo from local csv file or db')
def delete(
    db: bool = Option(help='Delete todo from the db', default=False),
    csv: bool = Option(help='Delete todo from the local csv file', default=False),
):
    if sum_true(db, csv) != 1:
        print(CHOOSE_BETWEEN_CSV_DB_MSG)

    todo_id = None
    try:
        todo_id = int(prompt('Todo Id : ', False))
    except ValueError:
        print('🛑 Enter a valid number')
        exit_app()

    db and Todos.delete(id=todo_id)

    try:
        csv and CSV.delete(id=todo_id)
    except IndexError:
        print("🛑Entered Todo Id is greater than the maximum id in the csv file")
        exit_app()

    print("Todo was deleted successfully")


if __name__ == '__main__':
    app()
