from fractions import Fraction as Frac
from eclipse_todo.helpers.utils import sum_true


def test_mixed_data_types_params():
    # Test to process primitive and non primitive types parameters
    args = (True, [], {}, "", None, 1, 0, -5, "t", Frac(0, 4), Frac(1, 7), 0.02)
    assert sum_true(*args) == 6


def test_true_param():
    assert sum_true(True) == 1


def test_true_params():
    args = ((1), [2], {"num": 3}, "str", 1, True)
    assert sum_true(*args) == 6


def test_false_param():
    assert sum_true(False) == 0


def test_false_params():
    # Pass only objects that evaluates to false in boolean expression
    args = ((), [], {}, '', 0, False, None)
    assert sum_true(*args) == 0


def test_no_params():
    assert sum_true() == 0
