# Source Backend Django

## Environment

Create `backend-django/.env` for local backend settings.

Current frontend origin:

```env
FRONTEND_URL=https://source-frontend-omega.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://source-frontend-omega.vercel.app
```

The backend now loads `backend-django/.env` automatically.

## Railway Postgres

The backend already uses `DATABASE_URL`, so Railway Postgres works without extra database code changes.

Set these variables in your Railway backend service:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
FRONTEND_URL=https://source-frontend-omega.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://source-frontend-omega.vercel.app
```

If your Railway database service has a different name, replace `Postgres` with that exact service name.

For local development, you can leave `DATABASE_URL` unset and Django will fall back to `db.sqlite3`.
