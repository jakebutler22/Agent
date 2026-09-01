# Hello Agent

Hello Agent is a small project for learning an agentic coding workflow. The
application will use a Vue interface and a FastAPI service while keeping the
frontend and backend as separate, reviewable parts of one project.

## Project structure

```text
hello-agent/
├── backend/     # Future FastAPI service
├── frontend/    # Future Vue interface
├── AGENTS.md
└── README.md
```

## Setup

The backend development environment uses Python 3.10 or newer. Create it and
install the declared dependencies with:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/python3 -m pip install -r backend/requirements.txt
```

Start the backend from the project root with:

```bash
backend/.venv/bin/python3 -m uvicorn backend.app.main:app --reload
```

The calculator API accepts numeric `a` and `b` query parameters and returns a
JSON result:

| Operation | Path |
| --- | --- |
| Add | `GET /api/add?a=7&b=5` |
| Subtract | `GET /api/subtract?a=7&b=5` |
| Multiply | `GET /api/multiply?a=7&b=5` |
| Divide | `GET /api/divide?a=7&b=2` |

A successful response has the form `{"result": 12.0}`. Division by zero returns
HTTP 400 with `{"detail": "Cannot divide by zero."}`.

The frontend uses Vue with JavaScript and requires a Node.js version matching
`^22.18.0 || >=24.12.0`. Install its dependencies and run its checks with:

```bash
cd frontend
npm install
npm run lint
npm run build
```

Run `npm run dev` from `frontend/` to start the development server. The frontend
provides inputs for both operands, an operation selector, and visible result and
error areas. During development, Vite proxies `/api` requests to the backend at
`http://127.0.0.1:8000`.
