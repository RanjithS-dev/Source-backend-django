# Source ERP - Backend (Django)

The backend service for the Source Coconut ERP, built with Python, Django, and Django Rest Framework.

## 🚀 Technology Stack
- **Framework**: Django 5.1
- **API**: Django Rest Framework (DRF)
- **Database**: SQLite (Local), PostgreSQL (Production/Railway)
- **Authentication**: JWT (SimpleJWT)
- **Deployment**: Railway / Vercel

## 📦 Core Modules
- **Users**: Custom UserProfile, roles (Admin, Supervisor, Worker), and Profile Image support.
- **Land**: Land owner management and Land Lease (Gudhagai) tracking with EMI/Ledger logic.
- **Employee**: Field staff and worker master records with wage tracking.
- **Vehicle**: Registration and transport tracking.
- **Worklog**: Daily harvesting logs linking lands, supervisors, and workers.
- **Sales**: Sales ledger linked to buyers, lands, and worklogs.
- **Expenses**: General operational expense tracking.

## 🛠️ Local Setup

1. **Clone and Enter Directory**:
   ```bash
   cd Source-backend-django
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file based on `.env.example`:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   FRONTEND_URL=http://localhost:3000
   ```

5. **Migrations & Superuser**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## ☁️ Deployment

### Railway (Recommended)
This repo includes a `railway.toml`. When deploying to Railway, ensure you:
1. Link a PostgreSQL service.
2. Set `DATABASE_URL` to `${{Postgres.DATABASE_URL}}`.
3. Set `DJANGO_ALLOWED_HOSTS` to your Railway domain.

### Vercel

The project ships with `vercel.json` + `build_files.sh` that handle everything automatically.

**Step 1 — Set environment variables in Vercel dashboard**

Go to your Vercel project → **Settings → Environment Variables** and add:

| Variable | Value |
|---|---|
| `SECRET_KEY` | Run `python -c "import secrets; print(secrets.token_hex(50))"` locally |
| `DEBUG` | `False` |
| `FRONTEND_URL` | Your Expo / web app URL (e.g. `https://source-frontend-omega.vercel.app`) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Same as FRONTEND_URL |
| `BOOTSTRAP_ADMIN_USERNAME` | `admin` (choose your login username) |
| `BOOTSTRAP_ADMIN_PASSWORD` | A strong password |
| `BOOTSTRAP_ADMIN_EMAIL` | your email (optional) |
| `DATABASE_URL` | *(optional)* Postgres URL from Neon/Supabase/Railway — leave blank to use SQLite (data resets on cold start) |

**Step 2 — Redeploy**

After saving the variables, trigger a redeploy from the Vercel dashboard (or `git push`).
The `build_files.sh` will:
1. Run `migrate` to create all database tables
2. Run `collectstatic`
3. Create your admin user via `bootstrap_admin`

**Step 3 — Login**

Use the `BOOTSTRAP_ADMIN_USERNAME` / `BOOTSTRAP_ADMIN_PASSWORD` you set above.

> **Note on SQLite vs Postgres:** Without `DATABASE_URL`, Vercel uses SQLite in `/tmp`.
> This is fine for demos — data persists within a single Lambda invocation but resets on cold starts.
> For real production data, connect a free Postgres from [neon.tech](https://neon.tech) or [supabase.com](https://supabase.com).

## 🛡️ License
Private Repository.
