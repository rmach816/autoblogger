# AutoBlogger v2 User Guide

## What You Get

- A web UI to generate and browse AI-generated articles
- A backend API that stores articles in SQLite via Prisma

## Using The Web UI

1. Start the backend:

```bash
cd backend
npm run dev
```

2. Start the frontend:

```bash
cd frontend
npm run dev
```

3. Open the UI (usually `http://localhost:5173`).

Tabs:

- Generate Article: create a new article by topic/keywords/word count
- My Articles: list previously generated articles and open them in a modal viewer

## API Endpoints (v2)

- `GET /health`: service health (returns `{ success, data }`)
- `POST /api/generate-article`: generate + persist an article
- `GET /api/articles`: list articles (returns summaries with `excerpt`)
- `GET /api/articles/:id`: fetch a full article
- `POST /api/generate-image`: placeholder (returns a static image URL)

