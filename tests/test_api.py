import io

VALID_CSV = """Дата;Номер группы;ФИО;Оценка
11.03.2025;101Б;Иван Золо;4
01.02.2025;103М;Леброн Джеймс;2
31.03.2025;103М;Леброн Джеймс;2
20.05.2025;103М;Ким Кардашьян;5
04.02.2025;102Б;Барак Обама;2
"""

INVALID_CSV_BAD_GRADE = """Дата;Номер группы;ФИО;Оценка
11.03.2025;101Б;Петухов Майот Айсгергевич;7
"""

import pytest

pytestmark = pytest.mark.asyncio


async def test_upload_ok(client):
    files = {"file": ("grades.csv", io.BytesIO(VALID_CSV.encode("utf-8")), "text/csv")}
    r = await client.post("/upload-grades", files=files)
    assert r.status_code == 200

    data = r.json()
    assert data["status"] == "ok"
    assert data["records_loaded"] == 5
    assert data["students"] == 4


async def test_upload_validation_error(client):
    files = {"file": ("grades.csv", io.BytesIO(INVALID_CSV_BAD_GRADE.encode("utf-8")), "text/csv")}
    r = await client.post("/upload-grades", files=files)
    assert r.status_code == 422

    body = r.json()
    assert body["detail"] == "Validation failed"
    assert len(body["errors"]) >= 1


async def test_analytics_endpoints(client):
    # загружаем валидные данные
    files = {"file": ("grades.csv", io.BytesIO(VALID_CSV.encode("utf-8")), "text/csv")}
    r = await client.post("/upload-grades", files=files)
    assert r.status_code == 200

    # more-than-3-twos (у нас никто не набрал >3 двоек)
    r = await client.get("/students/more-than-3-twos")
    assert r.status_code == 200
    assert r.json() == []

    # less-than-5-twos (у Третьякова 2 двойки, у Ковалёва 1)
    r = await client.get("/students/less-than-5-twos")
    assert r.status_code == 200
    data = r.json()

    # проверим, что Третьяков есть и count_twos = 2
    assert any(x["full_name"] == "Леброн Джеймс" and x["count_twos"] == 2 for x in data)
    assert any(x["full_name"] == "Барак Обама" and x["count_twos"] == 1 for x in data)