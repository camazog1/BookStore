#!/bin/bash

# Escalar auth-service
docker service scale auth-service=5

# Escalar catalog-service
docker service scale catalog-service=7

# Escalar transaction-service
docker service scale transaction-service=6

# Escalar api-gateway
docker service scale api-gateway=3

echo "✅ Escalamiento aplicado exitosamente."
