#!/bin/bash
# Crear servicios en el swarm

# auth-service
docker service create \
  --name auth-service \
  --replicas 3 \
  --publish 5001:5001 \
  --network bookstore_net_swarm \
  sebastianjimenez30/auth-service:latest

# catalog-service
docker service create \
  --name catalog-service \
  --replicas 5 \
  --publish 5002:5002 \
  --network bookstore_net_swarm \
  sebastianjimenez30/catalog-service:latest

# transaction-service
docker service create \
  --name transaction-service \
  --replicas 4 \
  --publish 5003:5003 \
  --network bookstore_net_swarm \
  sebastianjimenez30/transaction-service:latest

# api-gateway
docker service create \
  --name api-gateway \
  --replicas 2 \
  --publish 5000:5000 \
  --network bookstore_net_swarm \
  sebastianjimenez30/api-gateway:latest

echo "✅ Servicios desplegados exitosamente."
#!/bin/bash
# Crear servicios en el swarm

# auth-service
docker service create \
  --name auth-service \
  --replicas 3 \
  --publish 5001:5001 \
  --network bookstore_net_swarm \
  sebastianjimenez30/auth-service:latest

# catalog-service
docker service create \
  --name catalog-service \
  --replicas 5 \
  --publish 5002:5002 \
  --network bookstore_net_swarm \
  sebastianjimenez30/catalog-service:latest

# transaction-service
docker service create \
  --name transaction-service \
  --replicas 4 \
  --publish 5003:5003 \
  --network bookstore_net_swarm \
  sebastianjimenez30/transaction-service:latest

# api-gateway
docker service create \
  --name api-gateway \
  --replicas 2 \
  --publish 5000:5000 \
  --network bookstore_net_swarm \
  sebastianjimenez30/api-gateway:latest

echo "✅ Servicios desplegados exitosamente."
