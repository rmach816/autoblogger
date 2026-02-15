# AutoBlogger (v2)

AutoBlogger v2 is a simple full-stack app:

- `backend/`: Express API + Prisma + SQLite
- `frontend/`: React UI (Vite)

This repo also contains an older Python implementation in `autoblogger-legacy/`.

## Quick Start

Backend:

```bash
cd backend
copy env.example .env
npm install
npm run prisma:generate
npm run prisma:migrate
npm run dev
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the UI (usually) at `http://localhost:5173`.

## Notes

- If Prisma throws `Environment variable not found: DATABASE_URL`, check the encoding of `backend/.env`. It must be UTF-8 (not UTF-16).
- The backend can run without `GEMINI_API_KEY`; generation falls back to template content.

## Docs

- `docs/SETUP.md`
- `docs/CONFIGURATION.md`
- `docs/USER_GUIDE.md`

