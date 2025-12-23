import os
import pytest
import asyncpg
import httpx
import pytest_asyncio

import sys
from pathlib import Path

from app.db import connect_db, close_db

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ВАЖНО: env надо выставить ДО импорта app.settings (иначе Settings уже созданы)
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5431")  # твой порт на хосте
os.environ.setdefault("POSTGRES_DB", "grades")
os.environ.setdefault("POSTGRES_USER", "grades")
os.environ.setdefault("POSTGRES_PASSWORD", "grades")

from app.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    # чтобы httpx работал асинхронно
    return "asyncio"


@pytest_asyncio.fixture
async def db_conn():
    dsn = (
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    )
    conn = await asyncpg.connect(dsn)

    # чистим таблицу перед тестом, чтобы результаты не зависели от других запусков
    await conn.execute("TRUNCATE TABLE grades;")

    yield conn

    await conn.close()


@pytest_asyncio.fixture
async def client(db_conn):
    await connect_db()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    await close_db()