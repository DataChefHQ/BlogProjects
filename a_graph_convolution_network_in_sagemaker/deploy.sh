#! /bin/sh
docker build -t dgl-citation-network:custom-torch-1.8 -f Dockerfile .
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 939595455984.dkr.ecr.eu-west-1.amazonaws.com
docker tag dgl-citation-network:custom-torch-1.8 939595455984.dkr.ecr.eu-west-1.amazonaws.com/dgl-citation-network:custom-torch-1.8
docker push 939595455984.dkr.ecr.eu-west-1.amazonaws.com/dgl-citation-network:custom-torch-1.8