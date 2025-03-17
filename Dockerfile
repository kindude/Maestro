FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


CMD ["gunicorn", "Maestro.wsgi:application", "--bind", "0.0.0.0:8000"]
