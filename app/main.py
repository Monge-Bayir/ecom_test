from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import connect_db, close_db, get_pool
from app.routers.grades import router as grades_router
from app.routers.get_analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(title="Grades Service", version="0.1.0", lifespan=lifespan)

app.include_router(grades_router)
app.include_router(analytics_router)


@app.get("/health")
async def health():
    pool = get_pool()
    val = await pool.fetchval("SELECT 1;")
    return {"status": "ok", "db": val}