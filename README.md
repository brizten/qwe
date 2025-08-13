QWE — мини-сервис для расшифровки паролей и логирования
Веб-приложение на Flask для:

аутентификации администратора (пароль хранится в PostgreSQL),

расшифровки зашифрованных паролей с помощью Fernet-ключа из системного keyring,

копирования результата в буфер обмена,

записи «времени жизни» операции в Redis с авто-очисткой ключа. 
GitHub

Архитектура и основные компоненты
Flask + Flask-Session — веб-приложение, Cookie-сессии, маршруты / и /decode. 
GitHub

SQLAlchemy + PostgreSQL — модели admin_password и logs, авто-создание таблиц и вспомогательных PL/pgSQL функций/триггера при старте. Подключение по DSN (сейчас зашито локально). 
GitHub

cryptography.Fernet + keyring — дешифрование секретов Fernet-ключом, который извлекается из системного хранилища паролей (service='vault_key', username='key'). 
GitHub

pyperclip — копирование расшифрованного пароля в буфер обмена. 
GitHub

Redis — хранение временного маркера операции и мониторинг TTL в отдельном потоке; при малом TTL ключ удаляется. 
GitHub

Jinja2 шаблоны: templates/login.html, templates/decode.html; базовая стилизация в static/style/style.css. 
GitHub
+2
GitHub
+2

Примечание: функции db_pass и write_logs в db_func.py пока заглушки — их нужно реализовать под вашу схему БД/требования. 
GitHub

Требования
Python 3.10+

PostgreSQL 13+

Redis 6+

Системный keyring (Windows Credential Manager / macOS Keychain / Secret Service на Linux)

Зависимости Python
php
Копировать
Редактировать
Flask
Flask-Session
SQLAlchemy
psycopg2-binary
cryptography
pyperclip
keyring
redis
Установка и запуск (локально)
Клонируйте проект и установите зависимости

bash
Копировать
Редактировать
git clone https://github.com/brizten/qwe.git
cd qwe
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # если файла нет, см. список выше
Поднимите PostgreSQL и создайте БД (по умолчанию код ждёт БД pwd_m и локальный доступ)

Сейчас строка подключения зашита в db_modulev2.py как
postgresql+psycopg2://postgres:11355@127.0.0.1/pwd_m — обязательно замените под себя или вынесите в переменные окружения. 
GitHub

Поднимите Redis (локально на localhost:6379)
Мониторинг TTL запускается фоновым потоком при старте приложения. 
GitHub
+1

Заведите Fernet-ключ в системном keyring

Сгенерируйте ключ и сохраните его:

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
Приложение будет доставать его как:

python
Копировать
Редактировать
keyring.get_password('vault_key', 'key')
GitHub

Инициализируйте таблицы
При первом запуске SQLAlchemy создаст таблицы admin_password и logs, а также PL/pgSQL функции/триггер. 
GitHub

Добавьте запись с админ-паролем
В таблице admin_password должна быть строка с полем password — это пароль для входа на /. (В коде также предусмотрены поля prev_password и триггер обновления.) 
GitHub

Запустите приложение

bash
Копировать
Редактировать
python app.py
# или через Flask:
# export FLASK_APP=app.py && flask run
По умолчанию включён debug-режим и фоновый монитор Redis. 
GitHub

Как пользоваться
Откройте / — страница входа. Введите админ-пароль (берётся из admin_password). 
GitHub

После успешного входа попадёте на /decode.

Введите db_name и отправьте форму — сервис:

найдёт соответствующий зашифрованный пароль (требуется реализовать db_pass),

расшифрует его ключом из keyring,

скопирует в буфер обмена,

создаст в Redis ключ с TTL (по умолчанию 50 сек.), который мониторится фоновым процессом. 
GitHub
+1

Если что-то пойдёт не так, на странице появится сообщение об ошибке (валидация пустого db_name, «Database not found», «Decryption error» и т.д.). 
GitHub

Безопасность и настройки (важно)
SECRET_KEY: сейчас в app.py прописана строка 'your_secret_key'. Вынесите в переменные окружения. 
GitHub

DATABASE_URL: не храните логин/пароль к БД в коде, используйте ENV/DSN. 
GitHub

Fernet-ключ: держите только в системном keyring; не коммитьте в репозиторий. 
GitHub

Redis TTL: подберите TTL под ваши политики; сейчас ключи удаляются скриптом при малом оставшемся TTL. 
GitHub

Структура проекта
bash
Копировать
Редактировать
qwe/
├─ app.py                 # Flask-приложение, роуты, сессии, дешифровка, фоновый Redis-монитор
├─ db_modulev2.py         # SQLAlchemy engine, модели, DDL инициализация
├─ db_func.py             # утилиты для работы с БД (частично заглушки)
├─ redis_module.py        # обёртки над Redis + монитор TTL
├─ templates/
│  ├─ login.html          # форма входа
│  └─ decode.html         # форма расшифровки/сообщения
└─ static/
   └─ style/style.css     # базовые стили
GitHub
+6
GitHub
+6
GitHub
+6

TODO / дорожная карта
Реализовать db_pass(db_name) — поиск и возврат нужного зашифрованного пароля из вашей схемы БД. 
GitHub

Реализовать write_logs(db_name) — запись в таблицу logs факта расшифровки (включая время, систему и т.п.). 
GitHub

Вынести конфигурацию (SECRET_KEY, DSN БД, TTL, debug) в .env/переменные окружения. 
GitHub
+1

Добавить CSRF-защиту форм (Flask-WTF), rate-limit, аудит.

Отрисовать нормальные шаблоны (состояния ошибок/успеха, базовый layout). 
GitHub
+1

Написать тесты (юнит/интеграционные).


