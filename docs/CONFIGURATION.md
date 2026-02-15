# AutoBlogger v2 Configuration

AutoBlogger v2 is configured primarily via environment variables.

## Backend (`backend/.env`)

Minimum required:

```bash
DATABASE_URL="file:./dev.db"
```

Optional AI keys (if not provided, the backend falls back to template content):

```bash
GEMINI_API_KEY="..."
OPENAI_API_KEY="..."
```

Server settings:

```bash
PORT=5001
NODE_ENV="development"
```

CORS:

```bash
# Comma-separated list of allowed origins.
# Defaults: http://localhost:5173, http://localhost:3000
CORS_ORIGIN="http://localhost:5173"
```

Security:

```bash
JWT_SECRET="your_jwt_secret"
```

## Frontend (`frontend/.env`)

Optional:

```bash
VITE_API_BASE_URL=http://localhost:5001/api
```

