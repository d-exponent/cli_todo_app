import typer


def check_exit_abort(input: str):
    if 'exit' in input.lower():
        raise typer.Abort()
