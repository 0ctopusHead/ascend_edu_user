#!/bin/bash

# Create directory for certificates
sudo mkdir -p /certs

# Copy certificates from a secure location to /certs
sudo cp chain.pem /certs/chain.pem
sudo cp key.pem /certs/key.pem


docker compose down
docker compose pull
docker compose up -d
