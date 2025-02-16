# TimescaleDB Development Environment

This directory contains Docker Compose configuration for local development TimescaleDB instances with sharding:

- TimescaleDB Shard 1 Primary (port 5002)
- TimescaleDB Shard 1 Replica (port 5003)
- TimescaleDB Shard 2 Primary (port 5004)
- TimescaleDB Shard 2 Replica (port 5005)

## Setup Options

### Option 1: Manual Setup

1. Ensure your `.env` file contains the necessary TimescaleDB variables:

```bash
TIMESCALE_DB=your_database
TIMESCALE_USER=your_user
TIMESCALE_PASSWORD=your_password
TIMESCALE_REPLICATOR_PASSWORD=your_replication_password
```

2. Start the primary shards:

```bash
docker compose up -d timescale-shard1 timescale-shard2
```

3. Create replication users for both shards:

```bash
# Create replication user on shard1
source .env

docker exec -it agrosentry-timescale-shard1 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${TIMESCALE_REPLICATOR_PASSWORD}';"

# Create replication user on shard2
docker exec -it agrosentry-timescale-shard2 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${TIMESCALE_REPLICATOR_PASSWORD}';"
```

4. Initialize the replicas:

```bash
# Clean up volumes if they exist
docker volume rm -f agrosentry-db_timescale_shard1_replica_data
docker volume rm -f agrosentry-db_timescale_shard2_replica_data

# Initialize shard1 replica
docker run --rm \
  --network dev-db_default \
  -e PGPASSWORD=${TIMESCALE_REPLICATOR_PASSWORD} \
  -v agrosentry-db_timescale_shard1_replica_data:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg17 \
  pg_basebackup -h timescale-shard1 -p 5432 -D /var/lib/postgresql/data \
  -U replicator -v -P -R

# Initialize shard2 replica
docker run --rm \
  --network dev-db_default \
  -e PGPASSWORD=${TIMESCALE_REPLICATOR_PASSWORD} \
  -v agrosentry-db_timescale_shard2_replica_data:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg17 \
  pg_basebackup -h timescale-shard2 -p 5432 -D /var/lib/postgresql/data \
  -U replicator -v -P -R
```

5. Start the replicas:

```bash
docker compose up -d timescale-shard1-replica timescale-shard2-replica
```

### Option 2: Automated Setup

```bash
# Make script executable
chmod +x setup-timescale-replication.sh

# Run setup
./setup-timescale-replication.sh
```

## Verification

To verify the replication status:

```bash
# Check shard1 replication
docker exec -it agrosentry-timescale-shard1 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "SELECT * FROM pg_stat_replication;"

# Check shard2 replication
docker exec -it agrosentry-timescale-shard2 psql -U ${TIMESCALE_USER} -d ${TIMESCALE_DB} -c "SELECT * FROM pg_stat_replication;"
```

## Additional Notes

- Each shard runs TimescaleDB with PostgreSQL 17
- WAL level is set to replica mode
- Max WAL senders and replication slots are set to 10
- Make sure to adjust these values based on your needs
- The setup includes proper volume management for data persistence
