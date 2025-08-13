# QWE — мини-сервис для расшифровки паролей и логирования

Веб-приложение на **Flask** для:

- 🔑 аутентификации администратора (пароль хранится в **PostgreSQL**);
- 🔓 расшифровки зашифрованных паролей с помощью Fernet-ключа из системного **keyring**;
- 📋 копирования результата в буфер обмена;
- ⏳ записи «времени жизни» операции в **Redis** с авто-очисткой ключа.

---

## 📐 Архитектура и основные компоненты

- **Flask + Flask-Session** — веб-приложение, Cookie-сессии, маршруты `/` и `/decode`.
- **SQLAlchemy + PostgreSQL** — модели `admin_password` и `logs`, авто-создание таблиц и PL/pgSQL функций/триггера при старте. Подключение по DSN (зашито локально).
- **cryptography.Fernet + keyring** — дешифрование секретов Fernet-ключом, извлекаемым из системного хранилища паролей (`service='vault_key', username='key'`).
- **pyperclip** — копирование расшифрованного пароля в буфер обмена.
- **Redis** — хранение временного маркера операции и мониторинг TTL в отдельном потоке.
- **Jinja2** — шаблоны: `templates/login.html`, `templates/decode.html`; стили — `static/style/style.css`.

> ⚠️ Примечание: функции `db_pass` и `write_logs` в `db_func.py` пока заглушки — их нужно реализовать под вашу схему БД.

---

## 📋 Требования

- Python **3.10+**
- PostgreSQL **13+**
- Redis **6+**
- Системный **keyring** (Windows Credential Manager / macOS Keychain / Secret Service на Linux)

### Зависимости Python

```text
Flask
Flask-Session
SQLAlchemy
psycopg2-binary
cryptography
pyperclip
keyring
redis
🚀 Установка и запуск (локально)
Клонировать проект и установить зависимости

bash
Копировать
Редактировать
git clone https://github.com/brizten/qwe.git
cd qwe
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
Настроить PostgreSQL

По умолчанию код ждёт БД pwd_m и локальный доступ.

Строка подключения зашита в db_modulev2.py:

bash
Копировать
Редактировать
postgresql+psycopg2://postgres:11355@127.0.0.1/pwd_m
Замените под себя или вынесите в переменные окружения.

Запустить Redis

Локально на localhost:6379.

Мониторинг TTL стартует в фоне при запуске приложения.

Сохранить Fernet-ключ в системный keyring

bash
Копировать
Редактировать
python - <<'PY'
from cryptography.fernet import Fernet
import keyring
key = Fernet.generate_key().decode()
keyring.set_password('vault_key', 'key', key)
print('Fernet key saved in keyring.')
PY
Инициализировать таблицы

При первом запуске SQLAlchemy создаст таблицы admin_password и logs, а также PL/pgSQL функции и триггер.

Добавить запись с админ-паролем

В таблице admin_password должно быть поле password (пароль для входа на /).

Запустить приложение

bash
Копировать
Редактировать
python app.py
# или:
# export FLASK_APP=app.py && flask run
🛠 Как пользоваться
Перейдите на / — введите админ-пароль (из admin_password).

После входа — откроется /decode.

Введите db_name и отправьте форму:

сервис найдёт зашифрованный пароль (функция db_pass),

расшифрует его ключом из keyring,

скопирует в буфер обмена,

создаст в Redis ключ с TTL (по умолчанию 50 сек.).

При ошибке (пустой db_name, «Database not found», «Decryption error») появится сообщение.

🔒 Безопасность и настройки
SECRET_KEY — вынести в переменные окружения (сейчас 'your_secret_key' в app.py).

DATABASE_URL — не хранить в коде, использовать ENV.

Fernet-ключ — хранить только в keyring, не коммитить.

Redis TTL — подобрать под политику, ключи удаляются при малом остаточном TTL.

📂 Структура проекта
bash
Копировать
Редактировать
qwe/
├─ app.py                 # Flask-приложение, роуты, сессии, дешифровка, Redis-монитор
├─ db_modulev2.py         # SQLAlchemy engine, модели, DDL
├─ db_func.py             # функции для работы с БД (заглушки)
├─ redis_module.py        # обёртки над Redis + TTL-мониторинг
├─ templates/
│  ├─ login.html
│  └─ decode.html
└─ static/
   └─ style/style.css
📌 TODO / Дорожная карта
Реализовать db_pass(db_name) — поиск и возврат зашифрованного пароля.

Реализовать write_logs(db_name) — логирование расшифровок в logs.

Вынести конфигурацию в .env.

Добавить CSRF-защиту (Flask-WTF), rate-limit, аудит.

Улучшить шаблоны и UX.

Написать тесты.

