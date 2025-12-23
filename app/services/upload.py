import csv
import io
from datetime import datetime
from typing import Any

REQUIRED_COLUMNS = ["Дата", "Номер группы", "ФИО", "Оценка"]


def _norm(s: str) -> str:
    return " ".join(s.strip().split())


def parse_and_validate_csv(text: str) -> tuple[list[tuple[Any, ...]], list[dict], int]:
    """
    Возвращает:
      values: список кортежей для вставки (grade_date, group_number, full_name, grade)
      errors: список ошибок валидации
      students_count: кол-во уникальных студентов среди валидных строк
    """
    f = io.StringIO(text)
    reader = csv.DictReader(f, delimiter=";")

    if reader.fieldnames is None:
        return [], [{"row": 1, "field": "header", "error": "CSV has no header"}], 0

    header = [h.strip() for h in reader.fieldnames]
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        return [], [{"row": 1, "field": "header", "error": f"Missing columns: {missing}", "header": header}], 0

    values: list[tuple[Any, ...]] = []
    errors: list[dict] = []
    students = set()

    for row_num, row in enumerate(reader, start=2):
        date_raw = (row.get("Дата") or "").strip()
        group_raw = (row.get("Номер группы") or "").strip()
        name_raw = (row.get("ФИО") or "").strip()
        grade_raw = (row.get("Оценка") or "").strip()

        if not date_raw or not group_raw or not name_raw or not grade_raw:
            errors.append({"row": row_num, "error": "Empty field(s)"})
            continue

        try:
            grade_date = datetime.strptime(date_raw, "%d.%m.%Y").date()
        except ValueError:
            errors.append({"row": row_num, "field": "Дата", "error": "Expected DD.MM.YYYY"})
            continue

        try:
            grade = int(grade_raw)
        except ValueError:
            errors.append({"row": row_num, "field": "Оценка", "error": "Not an integer"})
            continue

        if grade < 2 or grade > 5:
            errors.append({"row": row_num, "field": "Оценка", "error": "Must be 2..5"})
            continue

        full_name = _norm(name_raw)
        group_number = _norm(group_raw)

        values.append((grade_date, group_number, full_name, grade))
        students.add(full_name)

    return values, errors, len(students)