# Use Python 3.10 as the base image
FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate --noinput

RUN echo "from django.contrib.auth import get_user_model; \
    User = get_user_model(); \
    User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" \
    | python manage.py shell


COPY check_social_app.py /app/
RUN echo "🔎 Checking SocialApp..." && python check_social_app.py | tee /dev/stderr


CMD ["gunicorn", "Maestro.wsgi:application", "--bind", "0.0.0.0:8000"]
