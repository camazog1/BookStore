#!/bin/bash
# Instala Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -aG docker ec2-user
newgrp docker

# Une este nodo al Swarm
docker swarm join --token <TOKEN-DE-WORKER> <IP-MANAGER>:2377
