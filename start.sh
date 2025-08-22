#!/bin/bash

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Starting Docker Compose..."
docker-compose build web
docker-compose up -d

echo "Resetting dev_db..."
docker exec -i dev_db psql -U irrnet_admin -d postgres -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE datname = 'irrnet_dev' AND pid <> pg_backend_pid();"

docker exec -i dev_db psql -U irrnet_admin -d postgres -c "DROP DATABASE IF EXISTS irrnet_dev;"
docker exec -i dev_db psql -U irrnet_admin -d postgres -c "CREATE DATABASE irrnet_dev;"

echo "Dumping data from postgres_db into dev_db..."
docker exec -i postgres_db pg_dump -U irrnet_admin -d irrnet_db | \
docker exec -i dev_db psql -U irrnet_admin -d irrnet_dev
