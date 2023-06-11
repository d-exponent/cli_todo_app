from typer import Exit


def exit_app(code: int = 0):
    raise Exit(code)
