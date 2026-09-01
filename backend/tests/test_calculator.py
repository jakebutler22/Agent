import pytest

from backend.app.calculator import add, divide, multiply, subtract


def test_add() -> None:
    assert add(7, 5) == 12


def test_add_negative_value() -> None:
    assert add(-7, 5) == -2


def test_subtract() -> None:
    assert subtract(7, 5) == 2


def test_multiply() -> None:
    assert multiply(7, 5) == 35


def test_divide() -> None:
    assert divide(7, 2) == pytest.approx(3.5)


def test_divide_by_zero() -> None:
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(7, 0)
