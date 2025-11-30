# Local Deployment Guide

## Overview

This guide walks you through running Platinum Sequence locally using Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git
- 8GB RAM minimum
- 10GB free disk space

## Quick Start

```bash
git clone <your-repo-url>
cd sobek
docker-compose up --build
```

Visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Architecture

The local environment consists of 4 services:

1. **Frontend** (Port 3000)
   - React + TypeScript + Tailwind
   - Nginx serving static files
   - Hot reload enabled in development

2. **Backend** (Port 8000)
   - FastAPI application
   - Auto-reload enabled
   - OpenAPI docs at /docs

3. **PostgreSQL** (Port 5432)
   - PostgreSQL 16
   - Persistent volume for data
   - Database: platinumsequence

4. **Qdrant** (Port 6333, 6334)
   - Vector database
   - Persistent volume for data
   - Ready for future AI features

## Development Workflow

### Starting Services

```bash
docker-compose up
```

Or with rebuild:
```bash
docker-compose up --build
```

Or using Make:
```bash
make dev
```

### Stopping Services

```bash
docker-compose down
```

Or:
```bash
make stop
```

### Viewing Logs

All services:
```bash
docker-compose logs -f
```

Specific service:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

Or using Make:
```bash
make logs
make backend-logs
make frontend-logs
```

### Making Changes

**Backend Changes:**
1. Edit files in `backend/app/`
2. FastAPI auto-reloads
3. Refresh http://localhost:8000/docs to see changes

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Vite hot-reloads automatically
3. Browser refreshes automatically

### Accessing Databases

**PostgreSQL:**
```bash
docker-compose exec postgres psql -U postgres -d platinumsequence
```

**Qdrant Dashboard:**
Visit http://localhost:6333/dashboard

## Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Default values work for local development.

## Troubleshooting

### Port Already in Use

If you get "port already allocated" errors:

1. Check what's using the port:
   ```bash
   lsof -i :3000
   lsof -i :8000
   ```

2. Stop the conflicting service or change ports in `docker-compose.yml`

### Container Build Failures

Clear Docker cache and rebuild:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Database Connection Issues

Reset database:
```bash
docker-compose down -v
docker-compose up
```

This removes all data, so only use in development.

### Frontend Not Loading

1. Check if backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check frontend logs:
   ```bash
   docker-compose logs frontend
   ```

## Clean Slate

To completely reset everything:

```bash
make clean
docker system prune -a
docker volume prune
```

Then rebuild:
```bash
docker-compose up --build
```

## Performance Tips

- Allocate more memory to Docker Desktop (8GB+ recommended)
- Use Docker volumes for better I/O performance
- Close unused applications to free up resources

## Next Steps

- Read [GCP_DEPLOYMENT.md](GCP_DEPLOYMENT.md) for production deployment
- Explore the API at http://localhost:8000/docs
- Customize the frontend in `frontend/src/App.tsx`

