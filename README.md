# Notes API

Учебный API на FastAPI для создания и хранения заметок. Данные сохраняются в PostgreSQL и остаются после перезапуска приложения.

## Как запустить

Нужны Python 3.10+, Git и установленный PostgreSQL с запущенной службой. Команды ниже — для Windows (`cmd`).

### 1. Подготовить проект

```bat
git clone https://github.com/NikitaSolovyovAK/web-http-lab.git
cd web-http-lab
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Если проект уже скачан, просто открой `cmd` в его папке и активируй окружение.

### 2. Подготовить базу

Открой SQL Shell (`psql`) и подключись как `postgres`: сервер `localhost`, база `postgres`, порт `5432`. Введи пароль, заданный при установке PostgreSQL.

Создай пользователя и базу:

```sql
CREATE USER notes_app WITH PASSWORD 'CHANGE_ME';
CREATE DATABASE notes_db OWNER notes_app;
```

Вместо `CHANGE_ME` укажи свой пароль. Если пользователь и база уже созданы, повторять эти команды не нужно.

Подключись к новой базе и выполни файл со схемой:

```text
\connect notes_db notes_app localhost 5432
\i 'C:/Users/user/Desktop/HW/web-http-lab/schema.sql'
```

При запросе пароля введи пароль `notes_app`. Путь к `schema.sql` замени своим, если проект лежит в другой папке. Ожидаемый ответ — `CREATE TABLE`.

Схема находится в [schema.sql](schema.sql). Пока пользователей в API нет, `user_id` для заметок автоматически равен `1`.

### 3. Запустить сервер

Вернись в `cmd` с активным окружением и выполни:

```bat
set "DATABASE_URL=postgresql://notes_app:CHANGE_ME@localhost:5432/notes_db"
python -m uvicorn main:app --reload
```

Используй тот же пароль, что при создании `notes_app`. Настройка действует в текущем окне `cmd`; в новом окне её нужно задать снова. Настоящий пароль в репозиторий не добавляй. Спецсимволы пароля в URL нужно кодировать.

Открой [документацию API](http://127.0.0.1:8000/docs) — оттуда можно отправлять запросы.

## Что умеет API

| Запрос | Действие |
| --- | --- |
| `GET /notes` | Получить все заметки |
| `POST /notes` | Создать заметку |
| `GET /notes/{note_id}` | Получить заметку по ID |
| `PATCH /notes/{note_id}` | Изменить заметку |
| `DELETE /notes/{note_id}` | Удалить заметку |
| `HEAD /notes/{note_id}` | Проверить, есть ли заметка |
| `GET /health` | Проверить работу API |
| `GET /hello` | Получить тестовое сообщение |

## Проверка сохранения

В `/docs` выбери **POST /notes → Try it out**, вставь JSON и нажми **Execute**:

```json
{
  "title": "Проверка PostgreSQL",
  "content": "Проверяем сохранение после перезапуска"
}
```

В ответе с кодом `201` появится `id` созданной заметки.

Останови сервер через **Ctrl+C**, запусти его снова той же командой и открой `http://127.0.0.1:8000/notes/1`, подставив свой ID вместо `1`. Должна вернуться прежняя заметка.

При локальной проверке заметка с ID `1` сохранилась после перезапуска.

## Скриншоты

<details>
<summary>Посмотреть запуск и результат проверки</summary>

Подключение к базе:

![Подключение к PostgreSQL](docs/screenshots/01-postgres-connection.png)

Документация API:

![Документация API](docs/screenshots/02-api-docs.png)

Запуск сервера:

![Запуск сервера](docs/screenshots/03-server-log.png)

Создание заметки:

![Ответ 201 и ID заметки](docs/screenshots/04-create-note.png)

Та же заметка после перезапуска:

![Заметка после перезапуска](docs/screenshots/05-note-after-restart.png)

</details>

## Отправка изменений на GitHub

Из папки проекта:

```bat
git add .
git commit -m "feat: persist notes in postgres"
git push
```

Перед commit проверь, что среди изменений нет настоящего пароля.
