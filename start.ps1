Write-Host "Running collectstatic..."
python manage.py collectstatic --noinput

Write-Host "Starting Docker Compose..."
docker-compose build web
docker-compose up -d

Write-Host "Dumping data from prod_db..."
docker exec postgres_db pg_dump -U irrnet_admin irrnet_db > prod_dump.sql

Write-Host "Restoring data to dev_db..."
docker cp .\prod_dump.sql dev_db:/tmp/prod_dump.sql
docker exec dev_db psql -U irrnet_admin -d irrnet_dev -f /tmp/prod_dump.sql
