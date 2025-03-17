# Use Python 3.10 as the base image
FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate --noinput

# Create superuser if it does not exist
RUN python manage.py shell -c \
    "from django.contrib.auth import get_user_model; \
    User = get_user_model(); \
    if not User.objects.filter(username='admin').exists(): \
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

# **NEW: Fix SocialApp issue & Start Gunicorn**
CMD sh -c "
    python manage.py shell -c '
from allauth.socialaccount.models import SocialApp;
apps = SocialApp.objects.filter(provider=\"google\");
for app in apps:
    print(f\"ID: {app.id}, Name: {app.name}, Sites: {app.sites.all()}\");
' && gunicorn Maestro.wsgi:application --bind 0.0.0.0:8000
"
