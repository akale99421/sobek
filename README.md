# Platinum Sequence

A modern, scalable business web application with React frontend and FastAPI backend, optimized for LLM development and seamless deployment.

## Features

- **Beautiful Coming Soon Page**: Modern gradient design with animations
- **FastAPI Backend**: Fast, async Python API with auto-generated documentation
- **React + TypeScript Frontend**: Type-safe, component-based UI
- **PostgreSQL + Qdrant**: Relational and vector databases ready for AI features
- **Containerized**: Docker Compose for local dev, Kubernetes for production
- **GKE Ready**: Production-ready deployment on Google Cloud Platform
- **LLM-Friendly**: Clear structure optimized for AI-assisted development

## Quick Start

### Local Development

```bash
docker-compose up --build
```

Visit:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Using Make

```bash
make dev      # Start all services
make stop     # Stop all services
make clean    # Remove all volumes
make logs     # View logs
```

## Project Structure

```
sobek/
├── frontend/              # React + TypeScript + Tailwind
├── backend/               # FastAPI application
├── infrastructure/
│   ├── k8s/              # Kubernetes manifests
│   └── terraform/        # GCP infrastructure
├── docs/                 # Documentation
├── docker-compose.yml    # Local development
├── Makefile             # Common commands
└── SETUP.txt            # Step-by-step setup guide
```

## Tech Stack

**Frontend:**
- React 18
- TypeScript 5
- Vite 5
- Tailwind CSS 3

**Backend:**
- FastAPI 0.104+
- Python 3.11
- Pydantic v2

**Databases:**
- PostgreSQL 16
- Qdrant (vector database)

**Infrastructure:**
- Docker & Docker Compose
- Kubernetes (GKE)
- Terraform
- Google Cloud Platform

## Documentation

- [SETUP.txt](SETUP.txt) - Quick setup checklist
- [Local Deployment](docs/LOCAL_DEPLOYMENT.md) - Detailed local setup
- [GCP Deployment](docs/GCP_DEPLOYMENT.md) - Production deployment guide

## Prerequisites

**For Local Development:**
- Docker Desktop
- Docker Compose
- Git

**For GCP Deployment:**
- GCP account
- gcloud CLI
- kubectl
- Terraform

## Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Default values work for local development.

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

Current endpoints:
- `GET /health` - Health check

## Development Workflow

1. **Start services**: `docker-compose up`
2. **Make changes**: Edit files in `backend/app/` or `frontend/src/`
3. **See changes**: Auto-reload enabled for both frontend and backend
4. **View logs**: `docker-compose logs -f [service]`
5. **Stop services**: `docker-compose down`

## Deployment

### Local
```bash
docker-compose up --build
```

### GCP Production
```bash
cd infrastructure/terraform
terraform init
terraform apply

# Build and push images
docker build -t gcr.io/PROJECT_ID/backend:latest backend/
docker push gcr.io/PROJECT_ID/backend:latest

# Deploy to Kubernetes
kubectl apply -f infrastructure/k8s/
```

See [GCP_DEPLOYMENT.md](docs/GCP_DEPLOYMENT.md) for detailed instructions.

## Domain

Production site: https://platinumsequence.com

## Future Roadmap

- [ ] Connect PostgreSQL and Qdrant to backend
- [ ] Add user authentication
- [ ] Implement API versioning (v1, v2)
- [ ] Add real business features
- [ ] Set up CI/CD with GitHub Actions
- [ ] Add monitoring and logging
- [ ] Implement vector search with Qdrant

## Contributing

This is a private project. For questions or issues, contact the development team.

## License

Proprietary - All rights reserved

