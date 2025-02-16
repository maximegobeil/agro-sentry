#!/bin/bash
set -e  # Exit on any error

if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please create .env file from .env.example"
    exit 1
fi

source .env

echo "Starting primary database..."
docker compose up -d db-primary

echo "Waiting for primary database to be ready..."
sleep 10  # Give PostgreSQL time to start

echo "Configuring replication access in pg_hba.conf..."
docker exec -i agrosentry-db-primary bash -c "echo 'host replication replicator all scram-sha-256' >> /var/lib/postgresql/data/pg_hba.conf"

echo "Reloading PostgreSQL configuration..."
docker exec -i agrosentry-db-primary psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT pg_reload_conf();"

echo "Creating replication user..."
docker exec -i agrosentry-db-primary psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${POSTGRES_REPLICATOR_PASSWORD}';"

echo "Cleaning up existing replica volumes..."
docker volume rm -f agrosentry-db_pg_replica_data || true

echo "Initializing replica from primary..."
docker run --rm \
  --network agrosentry_db_network \
  -e PGPASSWORD=${POSTGRES_REPLICATOR_PASSWORD} \
  -v agrosentry-db_pg_replica_data:/var/lib/postgresql/data \
  postgres:17.2 \
  pg_basebackup -h agrosentry-db-primary -p 5432 -D /var/lib/postgresql/data \
  -U replicator -v -P -R

echo "Starting replica..."
docker compose up -d db-replica

echo "Setup complete! Checking replication status..."
sleep 5  # Give replica time to start

# Check replication status
docker exec -i agrosentry-db-primary psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT * FROM pg_stat_replication;"