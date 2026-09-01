"""Framework-free calculator operations."""

Number = int | float


def add(left: Number, right: Number) -> Number:
    """Return the sum of two numbers."""
    return left + right


def subtract(left: Number, right: Number) -> Number:
    """Return the result of subtracting right from left."""
    return left - right


def multiply(left: Number, right: Number) -> Number:
    """Return the product of two numbers."""
    return left * right


def divide(left: Number, right: Number) -> float:
    """Return left divided by right.

    Raises:
        ZeroDivisionError: If right is zero.
    """
    if right == 0:
        raise ZeroDivisionError("Cannot divide by zero.")

    return left / right
