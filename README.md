# OpenCTI Docker Deployment for Testing

For Ubuntu:
```bash
sudo apt update
sudo apt-get update
sudo apt install docker.io
sudo apt install docker-compose
sudo apt install jq

cp env.sample .env
cd opencti-dev
docker-compose up
```