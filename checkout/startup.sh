#!/bin/bash
yum install docker -y
usermod -a -G docker ec2-user
systemctl  start docker
systemctl status docker
systemctl enable docker
curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose up -d