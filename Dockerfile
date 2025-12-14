FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Dar permisos de ejecución al script de notificaciones
RUN chmod +x /code/check_notifications.sh

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
