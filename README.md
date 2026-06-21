# auto-cr-tests

A small, deliberately realistic multi-language service used to exercise AI code-review tools.
It is not deployed anywhere - it just covers the usual surface area of a production app.

## Layout

| Path | Stack | What it is |
|------|-------|------------|
| `backend/` | Python 3.12 + FastAPI | Auth, users, middleware, utils, in-memory store |
| `frontend/` | TypeScript + React | Login form, user list, API client, token storage |
| `services/notifier/` | Node.js (JS) | Background worker that consumes a notification queue |

## Running (optional)

```bash
# backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# frontend
cd frontend && npm install && npm run dev

# notifier
cd services/notifier && npm install && node index.js
```
