#!/bin/bash
set -e  # Exit on any error

if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please create .env file from .env.example"
    exit 1
fi

source .env


echo "Starting TimescaleDB primary shards..."
docker compose up -d timescale-shard1 timescale-shard2

echo "Waiting for primary shards to be ready..."
sleep 10

echo "Configuring replication access in pg_hba.conf..."
docker exec -i agrosentry-timescale-shard1 bash -c "echo 'host replication replicator all scram-sha-256' >> /var/lib/postgresql/data/pg_hba.conf"
docker exec -i agrosentry-timescale-shard2 bash -c "echo 'host replication replicator all scram-sha-256' >> /var/lib/postgresql/data/pg_hba.conf"

echo "Reloading PostgreSQL configuration..."
docker exec -i agrosentry-timescale-shard1 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "SELECT pg_reload_conf();"
docker exec -i agrosentry-timescale-shard2 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "SELECT pg_reload_conf();"

echo "Creating replication user on shard1..."
docker exec -i agrosentry-timescale-shard1 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${TIMESCALE_REPLICATOR_PASSWORD}';"

echo "Creating replication user on shard2..."
docker exec -i agrosentry-timescale-shard2 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${TIMESCALE_REPLICATOR_PASSWORD}';"

echo "Cleaning up existing replica volumes..."
docker volume rm -f agrosentry-db_timescale_shard1_replica_data || true
docker volume rm -f agrosentry-db_timescale_shard2_replica_data || true

echo "Initializing shard1 replica..."
docker run --rm \
    --network agrosentry_timescale_db_network \
    -e PGPASSWORD=${TIMESCALE_REPLICATOR_PASSWORD} \
    -v agrosentry-db_timescale_shard1_replica_data:/var/lib/postgresql/data \
    timescale/timescaledb:latest-pg17 \
    pg_basebackup -h timescale-shard1 -p 5432 -D /var/lib/postgresql/data \
    -U replicator -v -P -R

docker run --rm \
    --network agrosentry_timescale_db_network \
    -e PGPASSWORD=${TIMESCALE_REPLICATOR_PASSWORD} \
    -v agrosentry-db_timescale_shard2_replica_data:/var/lib/postgresql/data \
    timescale/timescaledb:latest-pg17 \
    pg_basebackup -h timescale-shard2 -p 5432 -D /var/lib/postgresql/data \
    -U replicator -v -P -R

echo "Starting replica instances..."
docker compose up -d timescale-shard1-replica timescale-shard2-replica

echo "Waiting for replicas to start..."
sleep 10

echo "Verifying replication status for shard1..."
docker exec -i agrosentry-timescale-shard1 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} \
    -c "SELECT * FROM pg_stat_replication;"

echo "Verifying replication status for shard2..."
docker exec -i agrosentry-timescale-shard2 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} \
    -c "SELECT * FROM pg_stat_replication;"

echo "Setup complete!"