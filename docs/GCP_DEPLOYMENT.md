# GCP Deployment Guide

## Overview

This guide walks you through deploying Platinum Sequence to Google Cloud Platform using GKE (Google Kubernetes Engine).

## Prerequisites

- GCP account with billing enabled
- `gcloud` CLI installed
- `kubectl` installed
- `terraform` installed
- Docker installed
- Domain configured (platinumsequence.com)

## Architecture

Production deployment uses:
- **GKE**: Managed Kubernetes cluster
- **Artifact Registry**: Docker image storage
- **Cloud Load Balancer**: HTTPS ingress
- **Persistent Disks**: Database storage
- **Cloud DNS**: Domain management (optional)

## Step 1: GCP Project Setup

### Create Project

```bash
gcloud auth login
gcloud projects create platinumsequence --name="Platinum Sequence"
gcloud config set project platinumsequence
```

Or use existing project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

### Enable Required APIs

```bash
gcloud services enable container.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable dns.googleapis.com
```

### Set Up Billing

Link a billing account to your project via GCP Console.

## Step 2: Terraform Infrastructure

### Create State Bucket

```bash
gsutil mb -l us-central1 gs://platinumsequence-terraform-state
gsutil versioning set on gs://platinumsequence-terraform-state
```

### Configure Terraform

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
```hcl
project_id   = "platinumsequence"
region       = "us-central1"
environment  = "production"
node_count   = 2
machine_type = "e2-medium"
```

### Deploy Infrastructure

```bash
terraform init
terraform plan
terraform apply
```

This creates:
- GKE cluster with 2 nodes
- VPC network
- Artifact Registry
- Static IP address

Save the outputs:
```bash
terraform output
```

## Step 3: Configure kubectl

```bash
gcloud container clusters get-credentials platinumsequence-gke --region us-central1
kubectl cluster-info
```

## Step 4: Install cert-manager

For automatic HTTPS certificates:

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

Wait for cert-manager to be ready:
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=cert-manager -n cert-manager --timeout=300s
```

## Step 5: Build and Push Docker Images

### Configure Docker

```bash
gcloud auth configure-docker gcr.io
```

### Build Backend

```bash
cd ../../backend
docker build -t gcr.io/platinumsequence/backend:v1.0.0 .
docker push gcr.io/platinumsequence/backend:v1.0.0
docker tag gcr.io/platinumsequence/backend:v1.0.0 gcr.io/platinumsequence/backend:latest
docker push gcr.io/platinumsequence/backend:latest
```

### Build Frontend

```bash
cd ../frontend
docker build -t gcr.io/platinumsequence/frontend:v1.0.0 .
docker push gcr.io/platinumsequence/frontend:v1.0.0
docker tag gcr.io/platinumsequence/frontend:v1.0.0 gcr.io/platinumsequence/frontend:latest
docker push gcr.io/platinumsequence/frontend:latest
```

## Step 6: Configure Kubernetes

### Update Image References

```bash
cd ../infrastructure/k8s
sed -i 's/PROJECT_ID/platinumsequence/g' backend-deployment.yaml
sed -i 's/PROJECT_ID/platinumsequence/g' frontend-deployment.yaml
```

### Create Secrets

```bash
cp secrets.yaml.template secrets.yaml
```

Edit `secrets.yaml` with secure passwords:
```yaml
stringData:
  username: postgres
  password: YOUR_SECURE_PASSWORD_HERE
```

Apply secrets:
```bash
kubectl apply -f secrets.yaml
```

## Step 7: Deploy Application

### Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### Deploy Databases

```bash
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f qdrant-statefulset.yaml
```

Wait for databases to be ready:
```bash
kubectl wait --for=condition=ready pod -l app=postgres -n platinumsequence --timeout=300s
kubectl wait --for=condition=ready pod -l app=qdrant -n platinumsequence --timeout=300s
```

### Deploy Applications

```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

### Deploy Ingress

First, apply cert-manager issuer:
```bash
kubectl apply -f cert-manager.yaml
```

Then apply ingress:
```bash
kubectl apply -f ingress.yaml
```

## Step 8: Get External IP

```bash
kubectl get ingress -n platinumsequence -w
```

Wait for the `ADDRESS` column to show an IP (takes 5-10 minutes).

Example output:
```
NAME                        ADDRESS          PORTS
platinumsequence-ingress    34.120.45.67     80, 443
```

## Step 9: Configure DNS

### Option A: Namecheap

1. Log in to Namecheap
2. Go to Domain List → Manage → Advanced DNS
3. Add A Records:
   - Host: `@`, Value: `34.120.45.67`, TTL: Automatic
   - Host: `www`, Value: `34.120.45.67`, TTL: Automatic

### Option B: Cloud DNS

```bash
gcloud dns managed-zones create platinumsequence \
  --dns-name=platinumsequence.com. \
  --description="Platinum Sequence DNS"

gcloud dns record-sets transaction start --zone=platinumsequence
gcloud dns record-sets transaction add 34.120.45.67 \
  --name=platinumsequence.com. \
  --ttl=300 \
  --type=A \
  --zone=platinumsequence
gcloud dns record-sets transaction execute --zone=platinumsequence
```

Update nameservers at Namecheap with Cloud DNS nameservers.

## Step 10: Verify Deployment

### Check Pods

```bash
kubectl get pods -n platinumsequence
```

All pods should be `Running`.

### Check Services

```bash
kubectl get svc -n platinumsequence
```

### Check Ingress

```bash
kubectl describe ingress platinumsequence-ingress -n platinumsequence
```

### Test Application

```bash
curl http://platinumsequence.com/api/health
```

After DNS propagates (15 mins - 48 hours):
```
https://platinumsequence.com
```

## Monitoring

### View Logs

```bash
kubectl logs -f deployment/backend -n platinumsequence
kubectl logs -f deployment/frontend -n platinumsequence
```

### Check Resource Usage

```bash
kubectl top nodes
kubectl top pods -n platinumsequence
```

### GCP Console

Visit: https://console.cloud.google.com/kubernetes/workload

## Scaling

### Manual Scaling

```bash
kubectl scale deployment backend --replicas=3 -n platinumsequence
kubectl scale deployment frontend --replicas=3 -n platinumsequence
```

### Auto-scaling

Already configured in deployments. Kubernetes will auto-scale based on CPU usage.

## Updates

### Update Backend

```bash
cd backend
docker build -t gcr.io/platinumsequence/backend:v1.1.0 .
docker push gcr.io/platinumsequence/backend:v1.1.0
kubectl set image deployment/backend backend=gcr.io/platinumsequence/backend:v1.1.0 -n platinumsequence
```

### Update Frontend

```bash
cd frontend
docker build -t gcr.io/platinumsequence/frontend:v1.1.0 .
docker push gcr.io/platinumsequence/frontend:v1.1.0
kubectl set image deployment/frontend frontend=gcr.io/platinumsequence/frontend:v1.1.0 -n platinumsequence
```

### Rollback

```bash
kubectl rollout undo deployment/backend -n platinumsequence
kubectl rollout undo deployment/frontend -n platinumsequence
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod <pod-name> -n platinumsequence
kubectl logs <pod-name> -n platinumsequence
```

### Ingress Not Working

```bash
kubectl describe ingress platinumsequence-ingress -n platinumsequence
kubectl get events -n platinumsequence
```

### HTTPS Certificate Issues

```bash
kubectl get certificates -n platinumsequence
kubectl describe certificate platinumsequence-tls -n platinumsequence
```

### Database Connection Issues

```bash
kubectl exec -it postgres-0 -n platinumsequence -- psql -U postgres -d platinumsequence
```

## Cost Optimization

Current setup costs approximately $50-100/month:
- GKE cluster: ~$70/month
- Load Balancer: ~$18/month
- Storage: ~$5/month

To reduce costs:
1. Use smaller machine types (e2-small)
2. Reduce node count to 1 for development
3. Use preemptible nodes
4. Delete resources when not in use

## Cleanup

To delete everything:

```bash
kubectl delete namespace platinumsequence
cd infrastructure/terraform
terraform destroy
```

## Next Steps

- Set up monitoring with Cloud Monitoring
- Configure backups for PostgreSQL
- Set up CI/CD with GitHub Actions
- Enable Cloud CDN for better performance
- Configure alerting

