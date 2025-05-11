#!/bin/bash
# Instala Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -aG docker ec2-user
newgrp docker

# Inicializa Docker Swarm
docker swarm init --advertise-addr $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Crea la red overlay
docker network create --driver overlay bookstore_net_swarm

# (Opcional) Muestra el comando de join
echo "Token para workers:"
docker swarm join-token worker
