docker build -t europe-west1-docker.pkg.dev/ravens-regiment/cloud-run-source-deploy/raven-a3-api:latest .;
docker push europe-west1-docker.pkg.dev/ravens-regiment/cloud-run-source-deploy/raven-a3-api:latest;
gcloud run deploy raven-a3-api \
  --image="europe-west1-docker.pkg.dev/ravens-regiment/cloud-run-source-deploy/raven-a3-api:latest" \
  --region="europe-west1" \
  --allow-unauthenticated
gcloud run services replace service.yaml --region="europe-west1"