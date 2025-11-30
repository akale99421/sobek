# Quick Start Guide

## Get Running in 2 Minutes

### Prerequisites Check
```bash
docker --version    # Need Docker
docker-compose --version    # Need Docker Compose
```

### Start Everything
```bash
cd /home/alekh/sobek
docker-compose up --build
```

Wait 2-3 minutes for all services to start...

### Access Your App
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Stop Everything
```bash
Ctrl+C
docker-compose down
```

## Common Commands

```bash
make dev          # Start all services
make stop         # Stop all services
make clean        # Remove all data
make logs         # View all logs
make backend-logs # View backend only
```

## What's Running?

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | localhost:5432 |
| Qdrant | 6333 | http://localhost:6333 |

## Making Changes

### Backend
1. Edit `backend/app/main.py`
2. Save
3. FastAPI auto-reloads
4. Refresh http://localhost:8000/docs

### Frontend
1. Edit `frontend/src/App.tsx`
2. Save
3. Browser auto-refreshes

## Troubleshooting

**Port already in use?**
```bash
docker-compose down
# Change ports in docker-compose.yml
```

**Build failed?**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

**Reset everything?**
```bash
make clean
docker system prune -a
docker-compose up --build
```

## Deploy to Production

See `SETUP.txt` or `docs/GCP_DEPLOYMENT.md`

## Need Help?

- `SETUP.txt` - Step-by-step checklist
- `docs/LOCAL_DEPLOYMENT.md` - Detailed local guide
- `docs/GCP_DEPLOYMENT.md` - Production deployment
- `README.md` - Full documentation
- `PROJECT_SUMMARY.md` - What's been built

