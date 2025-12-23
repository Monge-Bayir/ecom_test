from fastapi import APIRouter

from app.db import get_pool
from app.services.analytics import more_than_3_twos, less_than_5_twos

router = APIRouter(prefix="/students", tags=["analytics"])


@router.get("/more-than-3-twos")
async def get_more_than_3_twos():
    pool = get_pool()
    recs = await more_than_3_twos(pool)
    return [{"full_name": r["full_name"], "count_twos": r["count_twos"]} for r in recs]


@router.get("/less-than-5-twos")
async def get_less_than_5_twos():
    pool = get_pool()
    recs = await less_than_5_twos(pool)
    return [{"full_name": r["full_name"], "count_twos": r["count_twos"]} for r in recs]