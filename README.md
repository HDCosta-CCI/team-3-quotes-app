# Team 3 - Quotes App Repository
## Backend (FastAPI) - Project Guide

This document covers setup, configuration, run/deploy for the backend Quotes app.

### Tech Stack
- FastAPI, Pydantic
- SQLAlchemy ORM
- Alembic (migrations)
- PostgreSQL (via `DATABASE_URL`)
- jose (JWT)

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Install all the packages in the venv and activate it.

### Environment Variables (.env)
Set in `backend/.env` (example):
```
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=your-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Install & Run
```
cd backend
fastapienv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
App runs on `http://127.0.0.1:8000` with docs at `/docs`.
