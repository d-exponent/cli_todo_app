from typer import Exit


def exit(code: int = 0):
    raise Exit(code)
