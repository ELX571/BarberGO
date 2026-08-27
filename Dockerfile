FROM python:3.12-slim

LABEL maintainer="ism@email.com"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ARG BUILD_VERSION=latest
RUN echo "Version: $BUILD_VERSION"

RUN python manage.py collectstatic --noinput

RUN useradd -m appuser
USER appuser

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
