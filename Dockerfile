FROM python:3.13 AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM base AS final

WORKDIR /app

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "config.wsgi:application"]
