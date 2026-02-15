# AutoBlogger v2 Setup (TypeScript + React)

This repo contains two implementations:

- v2 (current): `backend/` (Express + Prisma + SQLite) and `frontend/` (React + Vite)
- legacy (Python): `autoblogger-legacy/` (older CLI/web app)

The instructions below are for v2.

## Prereqs

- Node.js (recommended: 20+)

## Backend Setup

1. Create `backend/.env`:

   - Copy `backend/env.example` to `backend/.env`
   - Ensure the file is UTF-8 (not UTF-16). If Prisma complains `Environment variable not found: DATABASE_URL`, your `.env` encoding is usually the cause.

2. Install deps:

```bash
cd backend
npm install
```

3. Initialize Prisma (SQLite):

```bash
npm run prisma:generate
npm run prisma:migrate
```

4. Run the API:

```bash
npm run dev
```

Backend defaults:

- API: `http://localhost:5001/api`
- Health: `http://localhost:5001/health`

## Frontend Setup

1. Install deps:

```bash
cd frontend
npm install
```

2. Optional: configure API base URL.

By default the frontend uses `http://localhost:5001/api`.
To override, set:

- `frontend/.env`:

```bash
VITE_API_BASE_URL=http://localhost:5001/api
```

3. Run the UI:

```bash
npm run dev
```

Vite defaults to `http://localhost:5173`.

## Legacy (Python) Setup

If you want the older Python version, start from:

- `autoblogger-legacy/README.md`

