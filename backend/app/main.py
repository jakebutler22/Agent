"""FastAPI entry point for the Hello Agent calculator."""

from fastapi import FastAPI, HTTPException, status

from backend.app import calculator


app = FastAPI(title="Hello Agent Calculator")


@app.get("/api/add")
async def add(a: float, b: float) -> dict[str, float]:
    """Add two numbers."""
    return {"result": calculator.add(a, b)}


@app.get("/api/subtract")
async def subtract(a: float, b: float) -> dict[str, float]:
    """Subtract b from a."""
    return {"result": calculator.subtract(a, b)}


@app.get("/api/multiply")
async def multiply(a: float, b: float) -> dict[str, float]:
    """Multiply two numbers."""
    return {"result": calculator.multiply(a, b)}


@app.get("/api/divide")
async def divide(a: float, b: float) -> dict[str, float]:
    """Divide a by b."""
    try:
        result = calculator.divide(a, b)
    except ZeroDivisionError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return {"result": result}

