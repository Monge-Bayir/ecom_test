# Grades Service

Небольшой REST-сервис на FastAPI для загрузки CSV-файлов с успеваемостью студентов и простой аналитики по оценкам.

Сервис принимает CSV, валидирует данные, сохраняет их в PostgreSQL и предоставляет API для анализа количества оценок «2».  
ORM не используется — все операции выполняются напрямую через SQL.

---

## Стек
- Python 3
- FastAPI
- PostgreSQL
- asyncpg
- Docker / docker-compose
- pytest (для тестов)

---

## Формат входного CSV

Разделитель — `;`  
Первая строка — заголовки.

Обязательные колонки:
- `Дата` — формат `DD.MM.YYYY`
- `Номер группы`
- `ФИО`
- `Оценка` — целое число от 2 до 5

Поддерживаются файлы в кодировке UTF-8 (в том числе UTF-8 with BOM) и cp1251.

Каждая строка в CSV считается отдельным фактом выставления оценки.

---

## Запуск проекта

### Через Docker
```bash
docker compose up --build
```

После запуска:
-	Swagger UI: http://localhost:8000/docs
- Health-check: http://localhost:8000/health

## Тесты

Перед запуском тестов необходимо поднять контейнер с базой данных:
```bash
docker compose up -d db
```

Запуск
```bash
pytest -q
```

## Пример работы

<img width="1680" height="1050" alt="Снимок экрана 2025-12-23 в 14 46 17" src="https://github.com/user-attachments/assets/641c1822-2348-4cd8-b646-13fb518543de" />
<img width="1680" height="1050" alt="Снимок экрана 2025-12-23 в 14 46 07" src="https://github.com/user-attachments/assets/74d77099-65d8-4708-a27e-784aad8d588b" />
<img width="1680" height="1050" alt="Снимок экрана 2025-12-23 в 23 42 35" src="https://github.com/user-attachments/assets/82e4a212-fd58-4ddb-b5ba-eda0fcceff8e" />
<img width="1680" height="1050" alt="Снимок экрана 2025-12-23 в 23 42 41" src="https://github.com/user-attachments/assets/edd60de2-06f3-4874-b18d-e5139ce54724" />



