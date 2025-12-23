from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.db import get_pool
from app.schemas import UploadResponse
from app.services.upload import parse_and_validate_csv

router = APIRouter(tags=["grades"])


@router.post("/upload-grades", response_model=UploadResponse)
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    raw = await file.read()

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1251", errors="replace")

    values, errors, students_count = parse_and_validate_csv(text)

    if errors:
        # атомарно: при ошибках ничего не грузим
        return JSONResponse(status_code=422, content={"detail": "Validation failed", "errors": errors})

    pool = get_pool()
    sql = """
    INSERT INTO grades (grade_date, group_number, full_name, grade)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT DO NOTHING
    """

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(sql, values)

    return UploadResponse(status="ok", records_loaded=len(values), students=students_count)