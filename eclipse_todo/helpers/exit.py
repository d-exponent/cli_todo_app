from typer import Exit


def exit_app(code: int = 0):
    if code == 1:
        print("Aborting application")
    raise Exit(code)
