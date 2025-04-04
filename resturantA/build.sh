# # Run migrations (ensure the database is ready)
# python manage.py migrate

# # Create superuser non-interactively
# echo "Creating superuser..."
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
# User.objects.filter(username='$SUPERUSER_USERNAME').exists() or \
# User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell
# deploy.sh


# Wait for the database to be ready (retry until successful)
echo "Waiting for database..."
until python manage.py migrate 2>/dev/null; do
  echo "Retrying..."
  sleep 2
done

# Create superuser non-interactively
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='$SUPERUSER_USERNAME').exists() or \
User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell