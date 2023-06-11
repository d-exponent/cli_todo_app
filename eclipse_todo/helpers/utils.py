def sum_true(*args):
    total = 0
    if args is None:
        return total

    for arg in args:
        total += int(bool(arg))
    return total
