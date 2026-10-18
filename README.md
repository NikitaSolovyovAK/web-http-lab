# Notes API v0.1

Учебный REST API для управления заметками на FastAPI.

## 🚀 Установка и запуск

1. Создание виртуального окружения:
```bash
python -m venv .venv
```

2. Активация окружения:
- Windows: 
```bash
.venv\Scripts\activate
```
- Mac/Linux: 
```bash
source .venv/bin/activate
```

3. Установка зависимостей:
```bash
pip install -r requirements.txt
```

4. Запуск сервера:
```bash
uvicorn main:app --reload
```

## 📖 Документация
После запуска интерактивная документация доступна по адресу:
👉 **http://127.0.0.1:8000/docs**

## 🛠 Эндпоинты

* `GET /health` — проверка статуса сервера
* `GET /hello` — тестовый эндпоинт
* `GET /notes` — получить список всех заметок
* `POST /notes` — создать новую заметку
* `GET /notes/{note_id}` — получить заметку по ID
* `PATCH /notes/{note_id}` — частично обновить заметку (опционально)
* `DELETE /notes/{note_id}` — удалить заметку (опционально)
* `HEAD /notes/{note_id}` — проверить существование заметки (опционально)

## 📝 Примеры запросов и ответов

**Создание заметки (POST /notes):**

*Request body:*
```json
{
  "title": "title",
  "content": "content"
}
```

*Response (201 Created):*
```json
{
  "title": "title",
  "content": "content",
  "id": 1
}
```

## ⚠️ Ограничения
В текущей версии (v0.1) данные хранятся **in-memory** (в оперативной памяти). Это значит, что при перезапуске сервера все созданные заметки исчезают.