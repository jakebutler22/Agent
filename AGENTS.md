# Hello Agent Project Rules

These rules apply to the entire repository.

## Architecture

- Keep the FastAPI application in `backend/app/`.
- Keep Vue application code in `frontend/src/`.
- Put browser-facing API endpoints under `/api`.
- Keep route handlers thin; move reusable business logic into focused modules.
- Do not couple frontend components to backend implementation details beyond the
  documented API contract.

## Development

- Use Python type hints for backend code.
- Prefer async FastAPI route handlers for I/O-bound work.
- Use Vue 3 Composition API and `<script setup>` for new components.
- Keep components small and extract shared behavior when it has more than one
  consumer.
- Never commit secrets. Document required environment variables in `.env.example`.
- Do not commit virtual environments, `node_modules`, build output, or local editor
  settings.

## Dependencies

- Add dependencies only when they directly support a project requirement.
- Record Python dependencies in `backend/requirements.txt`.
- Record frontend dependencies in `frontend/package.json`.
- Commit lockfiles after the first dependency installation and keep them current.

## Verification

- Run relevant backend tests before finishing backend changes.
- Run relevant frontend tests and `npm run build` before finishing frontend changes.
- When test tooling does not exist yet, perform the closest available syntax or
  build check and state what could not be verified.
- Update `README.md` when setup steps, commands, ports, or architecture change.

## Course Macros

### AutoLoop

Trigger: When the user says `AutoLoop`, perform a bounded fix-and-verify loop.

1. Read `AGENTS.md`, `README.md`, and the relevant verification instructions.
2. State the acceptance check for the current task.
3. Run the smallest relevant check.
4. If the check fails for an in-scope source-code reason, inspect the evidence,
   make the smallest relevant correction, and rerun the check.
5. Repeat for no more than five correction cycles.
6. Stop early and ask for direction if the next action requires a dependency
   change, machine-level permission, destructive action, an unrelated process to
   be stopped, or broader scope.
7. Report every cycle, the final evidence, and anything not verified.

### SmokeTest

Trigger: When the user says `Run the smoke test`, verify the working application
without changing source code or dependency declarations.

1. Read `AGENTS.md`, `README.md`, and `docs/verification.md`.
2. Run the backend pytest suite.
3. Run the frontend lint and production build.
4. Check the intended backend and frontend ports. Never stop an unrelated process.
5. Start only the backend and frontend processes needed for this test in
   Codex-managed terminals.
6. Verify one successful API request and division-by-zero handling.
7. Use automated browser control to operate the visible calculator. Enter `7` and
   `6`, multiply them, and confirm that the displayed result is `42`.
8. Confirm that the browser displays no application error and report any UI
   behavior that could not be tested.
9. Unless the user asks to keep the app running, stop only the processes created by
   this smoke test.
10. Report concise evidence from tests, builds, endpoints, the automated UI
    interaction, and service cleanup.

### Combined trigger

When the user says `AutoLoop: run the smoke test`, run the SmokeTest macro. If an
in-scope check fails, use the AutoLoop rules to make the smallest correction and
repeat the smoke test until it passes, five correction cycles are exhausted, or a
stopping condition is reached.

