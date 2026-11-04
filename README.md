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

Таблицы создаются миграциями Alembic на следующем шаге. [schema.sql](schema.sql) содержит исходную схему таблицы. Пока пользователей в API нет, `user_id` для заметок автоматически равен `1`.

### 3. Применить миграции и запустить API

Вернись в `cmd` с активным окружением и выполни:

```bat
set "DATABASE_URL=postgresql://notes_app:CHANGE_ME@localhost:5432/notes_db"
python -m alembic upgrade head
python -m uvicorn main:app --reload
```

Используй тот же пароль, что при создании `notes_app`. Настройка действует в текущем окне `cmd`; в новом окне её нужно задать снова. Настоящий пароль в репозиторий не добавляй. Спецсимволы пароля в URL нужно кодировать.

Открой [документацию API](http://127.0.0.1:8000/docs) — оттуда можно отправлять запросы.

## Миграции (★)

Миграции лежат в `migrations/versions`:

- `001` — создаёт таблицу `notes`.
- `002` — добавляет `is_archived` со значением `FALSE` по умолчанию.

Текущая версия и история:

```bat
python -m alembic current
python -m alembic history
```

После обновления ожидается `002 (head)`. Alembic хранит версию в таблице `alembic_version`: повторный `upgrade head` уже применённые миграции не выполняет.

Если таблица создана старым `schema.sql`, миграции ещё не подключались и её структура совпадает с `001_create_notes_table.py`, можно зарегистрировать исходную версию и обновить базу:

```bat
python -m alembic stamp 001
python -m alembic upgrade head
```

Для пустой базы используется сразу `upgrade head`. Поле `is_archived` добавлено в БД; управление архивом через API пока не реализовано.

При проверке старая заметка сохранилась после обновления. На отдельной пустой базе обе миграции выполнились по порядку, а повторный запуск завершился без новых изменений.

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

Обновление базы до версии `002`:

![Применение второй миграции](docs/screenshots/06-migration-upgrade.png)

Миграции на пустой базе и повторный запуск:

![Проверка миграций с нуля](docs/screenshots/07-migrations-fresh-database.png)

</details>

## Отправка изменений на GitHub

Из папки проекта:

```bat
git add alembic.ini migrations requirements.txt README.md docs/screenshots
git diff --cached
git commit -m "feat: add Alembic migrations"
git push -u origin HEAD
```

Перед commit проверь, что среди изменений нет настоящего пароля.
