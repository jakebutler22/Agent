import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


@pytest.mark.parametrize(
    ("path", "a", "b", "expected"),
    [
        ("add", 7, 5, 12),
        ("subtract", 7, 5, 2),
        ("multiply", 7, 5, 35),
        ("divide", 7, 2, 3.5),
    ],
)
def test_calculator_path(
    path: str,
    a: float,
    b: float,
    expected: float,
) -> None:
    response = client.get(f"/api/{path}", params={"a": a, "b": b})

    assert response.status_code == 200
    assert response.json() == {"result": expected}


def test_division_by_zero_returns_client_error() -> None:
    response = client.get("/api/divide", params={"a": 7, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero."}


def test_non_numeric_parameter_is_rejected() -> None:
    response = client.get("/api/add", params={"a": "seven", "b": 5})

    assert response.status_code == 422

