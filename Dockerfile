# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости для операционной системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    && apt-get clean

# Создаем и переходим в директорию проекта
RUN mkdir /app
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "shopmoderno.wsgi:application"]