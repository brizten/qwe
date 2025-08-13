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


