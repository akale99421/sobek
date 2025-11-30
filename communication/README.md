# Communication Directory

This directory contains all coordination files for the development team.

## Team Structure

- **Head Executor**: Coordinates backend and frontend, makes architectural decisions
- **Backend Agent**: Implements APIs, database, business logic
- **Frontend Agent**: Implements UI, integrates with backend APIs

## Files

### For Backend Agent
- `BACKEND_TODOS.txt` - Your task list
- `BACKEND_INSTRUCTIONS.txt` - How to work and communicate
- `BACKEND_CHANGELOG.txt` - Document all your changes here

### For Frontend Agent
- `FRONTEND_TODOS.txt` - Your task list
- `FRONTEND_INSTRUCTIONS.txt` - How to work and communicate

### Shared
- `BACKEND_CHANGELOG.txt` - Frontend reviews this for new APIs

## Workflow

### Backend Agent Daily Routine
1. Check `BACKEND_TODOS.txt` for tasks
2. Implement features
3. Update `BACKEND_CHANGELOG.txt` with changes
4. Add frontend tasks to `FRONTEND_TODOS.txt` when APIs are ready
5. Mark todos complete

### Frontend Agent Daily Routine
1. Check `BACKEND_CHANGELOG.txt` for new APIs
2. Check `BACKEND_TODOS.txt` to see what's coming
3. Check `FRONTEND_TODOS.txt` for your tasks
4. Implement unblocked features
5. Mark todos complete

### Head Executor
- Reviews all files
- Unblocks agents
- Makes architectural decisions
- Handles infrastructure
- Coordinates between agents

## Communication Protocol

### Backend → Frontend
- Document new APIs in `BACKEND_CHANGELOG.txt`
- Add integration tasks to `FRONTEND_TODOS.txt`
- Include request/response examples

### Frontend → Backend
- Mark tasks as [BLOCKED] in `FRONTEND_TODOS.txt`
- Note what API is needed
- Head Executor will coordinate

### Both → Head Executor
- Report blockers
- Request infrastructure changes
- Ask architectural questions

## Current Status

**Backend**: Working on file upload to MinIO
**Frontend**: Waiting for upload API, can work on UI improvements
**Infrastructure**: All services running (PostgreSQL, Qdrant, MinIO, pgAdmin)

## Quick Links

- Backend API Docs: http://localhost:8000/docs
- Frontend Dev: http://localhost:5173
- pgAdmin: http://localhost:5050
- MinIO Console: http://localhost:9001

