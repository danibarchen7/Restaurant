# # Run migrations (ensure the database is ready)
# python manage.py migrate

# # Create superuser non-interactively
# echo "Creating superuser..."
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
# User.objects.filter(username='$SUPERUSER_USERNAME').exists() or \
# User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell
#!/bin/bash
set -e  # Exit on error

# Wait for PostgreSQL (Render-specific)
echo "Waiting for PostgreSQL to be ready..."
python manage.py check --database default --deploy 2>&1 >/dev/null 

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser (non-interactive)
echo "Creating superuser (if not exists)…"
python -u <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['SUPERUSER_USERNAME']
email = os.environ['SUPERUSER_EMAIL']
password = os.environ['SUPERUSER_PASSWORD']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists.")
EOF