def sum_objects(*args):
    sum = 0
    for arg in args:
        sum += int(bool(arg))
    return sum
