# Dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установка зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование исходного кода
COPY . /app/

CMD ["gunicorn", "awards_api.wsgi:application", "--bind", "0.0.0.0:8000"]
