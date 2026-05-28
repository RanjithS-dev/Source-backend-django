#!/usr/bin/env bash
# build_files.sh — runs during Vercel build step
# This creates the SQLite database with all tables and optionally a first admin user.
set -e

echo ">>> Installing Python dependencies..."
pip install -r requirements.txt

echo ">>> Running database migrations..."
python manage.py migrate --noinput

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput --clear

# ─────────────────────────────────────────────────────────────────────────────
# Bootstrap the first admin user.
# Set these three env vars in your Vercel project settings → Environment Variables:
#   BOOTSTRAP_ADMIN_USERNAME   e.g.  admin
#   BOOTSTRAP_ADMIN_PASSWORD   e.g.  YourStrongPassword123
#   BOOTSTRAP_ADMIN_EMAIL      e.g.  admin@yourcompany.com  (optional)
# This command is idempotent — safe to redeploy without creating duplicates.
# ─────────────────────────────────────────────────────────────────────────────
if [ -n "${BOOTSTRAP_ADMIN_USERNAME}" ] && [ -n "${BOOTSTRAP_ADMIN_PASSWORD}" ]; then
    echo ">>> Bootstrapping admin user: ${BOOTSTRAP_ADMIN_USERNAME}"
    python manage.py bootstrap_admin \
        --username "${BOOTSTRAP_ADMIN_USERNAME}" \
        --password "${BOOTSTRAP_ADMIN_PASSWORD}" \
        --email "${BOOTSTRAP_ADMIN_EMAIL:-}" \
        --full-name "${BOOTSTRAP_ADMIN_FULL_NAME:-Workspace Admin}"
    echo ">>> Admin user ready."
else
    echo ">>> WARNING: BOOTSTRAP_ADMIN_USERNAME / BOOTSTRAP_ADMIN_PASSWORD not set."
    echo ">>>          Login will fail until you create a user. See README.md."
fi

if [ -n "${BOOTSTRAP_ADMIN2_USERNAME}" ] && [ -n "${BOOTSTRAP_ADMIN2_PASSWORD}" ]; then
    echo ">>> Bootstrapping second admin user: ${BOOTSTRAP_ADMIN2_USERNAME}"
    python manage.py bootstrap_admin \
        --username "${BOOTSTRAP_ADMIN2_USERNAME}" \
        --password "${BOOTSTRAP_ADMIN2_PASSWORD}" \
        --email "${BOOTSTRAP_ADMIN2_EMAIL:-}" \
        --full-name "${BOOTSTRAP_ADMIN2_FULL_NAME:-Workspace Admin}"
    echo ">>> Second admin user ready."
fi

echo ">>> Build complete."
