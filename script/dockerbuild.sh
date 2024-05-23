#!/bin/sh

DTAG=$(date +"%Y%m%d%H%M%S")

echo "Building Docker image..."
if docker build --platform linux/amd64 -f Dockerfile -t hogwarts-tg-gateway .; then
  echo "Docker image built successfully."
else
  echo "Docker build failed."
  exit 1
fi

echo "Tagging Docker image..."
if docker tag hogwarts-tg-gateway registry.digitalocean.com/francisco/hogwarts-tg-gateway:$DTAG; then
  echo "Docker image tagged successfully."
else
  echo "Docker tag failed."
  exit 1
fi

echo "Pushing Docker image..."
if docker push registry.digitalocean.com/francisco/hogwarts-tg-gateway:$DTAG; then
  echo "registry.digitalocean.com/francisco/hogwarts-tg-gateway:$DTAG image push success"
else
  echo "Docker push failed."
  exit 1
fi