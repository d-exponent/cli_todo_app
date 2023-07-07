import os
import csv
import pandas as pd
from datetime import datetime
from dataclasses import dataclass

from eclipse_todo.constants import TODOS

NOW = datetime.now()


@dataclass
class TodoEntry:
    todo: str
    due: datetime | None = None


class CSV:
    @classmethod
    def create(cls, new_todo):
        # Create the csv todos file if it doesn't exist
        if not os.path.exists(TODOS):
            with open(TODOS, 'x'):
                pass

        # Retrieve the csv file headers if any
        with open(TODOS, 'r') as f:
            headers = next(csv.reader(f), None)
            has_headers = bool(headers)

        # Add the new todo
        df = pd.DataFrame(
            {
                'todo': [new_todo.todo],
                'due': [str(new_todo.due.date()) if new_todo.due else 'None'],
                'created_at': str(NOW).split('.')[0],
            }
        )

        df.to_csv(TODOS, mode='a', header=not has_headers, index=False)

    @classmethod
    def update(cls, id: int, new_todo: str):
        df = pd.read_csv(TODOS)
        df.loc[id - 1, 'todo'] = new_todo  # See helpers.draw line 26,27
        df.to_csv(TODOS, index=False, header=True)

    @classmethod
    def delete(cls, id: int):
        df = pd.read_csv(TODOS)
        df = df.drop(df.index[id - 1])  # see line 45
        df = df.to_csv(TODOS, index=False, header=True)
