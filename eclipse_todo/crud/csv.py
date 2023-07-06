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
        is_todos_exist = os.path.exists(TODOS)

        # Create the csv todos file if it doesn't exist
        if not is_todos_exist:
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
