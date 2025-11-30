# Hot Reload Guide

## 🔥 Hot Reload Status

| Component | Hot Reload | How It Works |
|-----------|-----------|--------------|
| **Backend** | ✅ YES | Uvicorn `--reload` flag |
| **Frontend** | ✅ YES (with dev mode) | Vite dev server |

## Backend Hot Reload (Already Working!)

The backend **already has hot reload** enabled:

```bash
# Just run normally
docker compose up
```

**Test it:**
1. Edit `backend/app/main.py`
2. Add a new endpoint or change something
3. Save the file
4. Watch the terminal - you'll see: `Reloading...`
5. Refresh http://localhost:8000/docs - changes appear!

**Example:**
```python
# Add this to backend/app/main.py
@app.get("/test")
async def test():
    return {"message": "Hot reload works!"}
```

Save → Wait 2 seconds → Visit http://localhost:8000/test

## Frontend Hot Reload (Use Dev Mode)

### Option 1: Development Mode (Hot Reload) ⚡

```bash
# Stop current containers
docker compose down

# Start with hot reload
make dev-hot

# Or manually:
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

**Frontend now at:** http://localhost:5173 (dev mode uses Vite's default port)

**Test it:**
1. Edit `frontend/src/App.tsx`
2. Change some text
3. Save the file
4. Browser automatically refreshes! ⚡

### Option 2: Production Mode (No Hot Reload)

```bash
# Normal mode (what you've been using)
docker compose up --build
```

This builds the production version - faster but no hot reload.

## Quick Comparison

### Development Mode (`make dev-hot`)
- ✅ Frontend hot reload
- ✅ Backend hot reload
- ✅ Instant changes
- ❌ Slower initial startup
- **Use for:** Active development

### Production Mode (`docker compose up`)
- ✅ Backend hot reload
- ❌ Frontend requires rebuild
- ✅ Faster startup
- ✅ Closer to production
- **Use for:** Testing production builds

## Recommended Workflow

### Daily Development
```bash
# Start with hot reload
make dev-hot

# Edit files
# - backend/app/*.py → auto-reloads
# - frontend/src/*.tsx → auto-refreshes

# Stop when done
Ctrl+C
docker compose down
```

### Before Deploying
```bash
# Test production build
docker compose up --build

# Make sure everything works
# Then deploy to GCP
```

## What Gets Hot Reloaded?

### Backend (Always)
- ✅ `backend/app/main.py`
- ✅ `backend/app/core/config.py`
- ✅ Any Python file in `backend/app/`
- ❌ `requirements.txt` (need rebuild)
- ❌ `Dockerfile` (need rebuild)

### Frontend (Dev Mode Only)
- ✅ `frontend/src/App.tsx`
- ✅ `frontend/src/index.css`
- ✅ Any file in `frontend/src/`
- ✅ `frontend/index.html`
- ✅ Tailwind classes (auto-compiles)
- ❌ `package.json` (need rebuild)
- ❌ `vite.config.ts` (need restart)

## Troubleshooting

### Backend not reloading?
```bash
# Check if --reload flag is there
docker compose logs backend | grep reload

# Should see: "Uvicorn running with --reload"
```

### Frontend not reloading?
```bash
# Make sure you're using dev mode
make dev-hot

# Check frontend is using Vite dev server
docker compose logs frontend | grep vite
```

### Changes not appearing?
```bash
# Hard refresh browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Or clear Docker volumes
docker compose down -v
docker compose up --build
```

## Summary

**For development (hot reload everywhere):**
```bash
make dev-hot
```

**For production testing:**
```bash
make dev
```

Both have backend hot reload. Dev mode adds frontend hot reload! 🔥

