#!/bin/bash

# Cluster name
CLUSTER_NAME="agrosentry-cluster"

# Delete cluster if it exists
echo "Cleaning up any existing cluster..."
minikube delete -p $CLUSTER_NAME

# Start cluster with specific configuration
echo "Starting new cluster..."
minikube start \
  --cpus=2 \
  --memory=3072 \
  --disk-size=20g \
  -p $CLUSTER_NAME

# Wait for nodes to be ready
echo "Waiting for nodes to be ready..."
sleep 15

# Point shell to minikube's docker daemon
echo "Configuring docker environment..."
eval $(minikube -p $CLUSTER_NAME docker-env)

# Build images
echo "Building Docker images..."
docker build -t agrosentry-web:latest -f web/Dockerfile .
#docker build -t agrosentry-iot:latest -f iot/Dockerfile .
#docker build -t agrosentry-notification:latest -f notification/Dockerfile .

# Verify setup
echo "Cluster nodes:"
kubectl get nodes --show-labels

echo "Docker images:"
docker images | grep agrosentry

echo "Setup complete! Now you can:"
echo "1. Deploy RabbitMQ and IoT pods"
echo "2. Deploy Web and Notification pods"
echo "3. Access services using 'minikube -p $CLUSTER_NAME service <service-name>'"