# Verification

Use these checks from the project root unless a step says otherwise. Do not install
or update dependencies during verification.

## Automated checks

Run the backend suite without creating Python or pytest cache files:

```bash
backend/.venv/bin/python3 -B -m pytest -p no:cacheprovider backend/tests
```

Run non-fixing frontend lint checks, then build from `frontend/`:

```bash
./node_modules/.bin/oxlint .
./node_modules/.bin/eslint .
npm run build
```

## Smoke test

1. Confirm ports 8000 and 5173 are free. If either is occupied, identify the
   listener and stop for direction; never stop an unrelated process.
2. Start FastAPI in a Codex-managed terminal:

   ```bash
   backend/.venv/bin/python3 -B -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
   ```

3. Start Vite in a separate Codex-managed terminal from `frontend/`:

   ```bash
   npm run dev -- --host 127.0.0.1 --port 5173
   ```

4. Request `GET http://127.0.0.1:5173/api/multiply?a=7&b=6` through the Vite proxy.
   Expect HTTP 200 and `{"result":42.0}`.
5. Request `GET http://127.0.0.1:5173/api/divide?a=7&b=0`. Expect HTTP 400 and
   `{"detail":"Cannot divide by zero."}`.
6. With automated browser control, open `http://127.0.0.1:5173`, enter `7` and `6`,
   choose Multiply, select Calculate, and confirm the visible result is `42` and
   the error area shows no application error.
7. Unless asked to keep the application running, stop only the FastAPI and Vite
   processes started for this smoke test. Confirm both ports are closed.

Report pass/fail evidence for every stage and identify anything that could not be
verified.

