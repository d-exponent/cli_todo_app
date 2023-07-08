def new_line():
    print("\n")


def new_line_then_print(msg: str = ""):
    new_line()
    print(msg)


def sum_true(*args):
    if args is None:
        return 0

    return sum([int(bool(i)) for i in args])
