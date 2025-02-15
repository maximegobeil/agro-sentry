# Development Databases

This directory contains Docker Compose configuration for local development databases:

- PostgreSQL Primary (port 5000)
- PostgreSQL Replica (port 5001)

## Setup Options

### Option 1: Manual Setup

1. setup .env file in this directory

2. Start the databases:

```bash
docker compose up -d db-primary
```

3. Create replication user

```bash
# Create replication user on primary
source .env

docker exec -it agrosentry-db-primary psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${POSTGRES_REPLICATOR_PASSWORD}';"
\q

# Clean up volume if it exists
docker volume rm -f agrosentry-db_pg_replica_data

# Initialize replica
docker run --rm \
  --network dev-db_default \
  -e PGPASSWORD=${POSTGRES_REPLICATOR_PASSWORD} \
  -v agrosentry-db_pg_replica_data:/var/lib/postgresql/data \
  postgres:17.2 \
  pg_basebackup -h db-primary -p 5432 -D /var/lib/postgresql/data \
  -U replicator -v -P -R

# Start replica
docker compose up -d db-replica
```

### Option 2: Automated Setup

```bash
# Make script executable
chmod +x setup-replication.sh

# Run setup
./setup-replication.sh
```
