#!/bin/bash
set -e

# Only collect static files during build
# Migrations should be run separately after deployment on Vercel
# Use: vercel env pull && vercel env list, then run migrations via console or scheduled job

python manage.py collectstatic --noinput
