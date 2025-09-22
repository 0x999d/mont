<p align="center">🌐 mont</p>


<p align="center">Приложение для мониторинга доступности и работоспособности веб сайтов</p>


## 🚀 Возможности

- ⏱ Периодическая проверка списка любого количества URL
- ✅ Отслеживание HTTP статус кодов 
- 📝 Отслеживание содержимого URL страницы
- 📉 Логирование времени ответа и доступности
- 🗃 История проверок

## Архитектура проекта

Проект состоит из двух основных компонентов, второй является опциональном, но сильно дополняет возможности 

### api/

Серверная часть, реализованная на `FastAPI`

### telegram-bot/

Пример клиента на базе Telegram бота ( `aiogram3` ), использующего API

Функциональность:

- 🔁 Все, что есть в API
- 📊 Построение графика доступности на основе истории проверок и времени отклика
- ⏱ Подсчёт времени uptime и downtime
- 🚨 Возможность получать уведомления о смене содержимого на сайте, падениях и возвращении в норму
- 📤 Экспорт истории в `XLSX` формат

## 📦 Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/0x999d/mont.git
cd mont
```
### 2 Создание RSA ключей для JWT
```bash
mkdir api/keys
openssl genpkey -algorithm RSA -out api/keys/private.pem -pkeyopt rsa_keygen_bits:2048 

openssl rsa -pubout -in api/keys/private.pem -out api/keys/public.pem
```

### Настройка параметров и переменных API
```bash
export DB_CONNECT_URL=sqlite+aiosqlite:///data.db

sed -i "s/OPENAI_DB_CONNECT_URLAPI_KEY=DB_CONNECT_URL/DB_CONNECT_URL=${DB_CONNECT_URL}/" api/Dockerfile 
```

Для более тонкой настройки необходимо отредактировать файл конфигурации

```bash
nano api/const.py
```

---

При отсутствии желания использовать клиенсткую часть, можно собрать и запустить API прямо сейчас  

```bash
cd api
docker build .
docker run -d -p 8080:8080 api
```

### Настройка параметров и переменных клиента
```bash
export TOKEN_TELEGRAM_BOT=your_telegram_token
export CIPHER_KEY=supersecretkey
export DB_CONNECT_URL=sqlite+aiosqlite:///data.db

sed -i "s/TOKEN_TELEGRAM_BOT=TOKEN_TELEGRAM_BOT/TOKEN_TELEGRAM_BOT=${TOKEN_TELEGRAM_BOT}/" telegram-bot/Dockerfile 

sed -i "s/CIPHER_KEY=supersecurekey/CIPHER_KEY=${CIPHER_KEY}/" telegram-bot/Dockerfile 

sed -i "s/DB_CONNECT_URL=DB_CONNECT_URL/DB_CONNECT_URL=${DB_CONNECT_URL}/" telegram-bot/Dockerfile 
```

Для более тонкой настройки необходимо отредактировать файл конфигурации

```bash
nano telegram-bot/const/conf.py # Основные параметры
nano telegram-bot/const/message.py # Ответы бота
```

### Сборка контейнеров
```bash
docker compose up -d --build
```

---

## Схема базы данных

### `users`

```markdown
| Поле     | Тип     | Ключи                       |
|----------|---------|-----------------------------|
| username | String  | Primary Key                 |
| password | String  | Not Null                    |
```

---

### `trackedurls`

```markdown
| Поле     | Тип     | Ключи                                                       |
|----------|---------|-------------------------------------------------------------|
| id       | Integer | Primary Key, Auto Increment                                 |
| interval | Integer | Not Null                                                    |
| url      | String  | Not Null                                                    |
| owner    | String  | Foreign Key → `users.username`, Not Null, On Delete CASCADE |
```

---

### `trackhistory`

```markdown
| Поле          | Тип      | Ключи                                                           |
|---------------|----------|-----------------------------------------------------------------|
| id            | Integer  | Primary Key, Auto Increment                                     |
| latency       | Float    | Nullable                                                        |
| http_status   | Integer  | Nullable                                                        |
| is_ok         | Boolean  | Not Null, Default = True                                        |
| hash_reqbytes | String   | Nullable                                                        |
| date          | DateTime | Not Null, Default = `datetime.now`                              |
| site_id       | Integer  | Foreign Key → `trackedurls.id`, Not Null, On Delete CASCADE     |
```

---

### Связи

```markdown
- `users.username` ← `trackedurls.owner` — один ко многим
- `trackedurls.id` ← `trackhistory.site_id` — один ко многим
```

## 📡 API методы

Все методы, кроме регистрации и логина, требуют заголовок:


| Метод | Путь             | Описание                                      |
|-------|------------------|-----------------------------------------------|
| `POST`   | `/register`        | 🔐 Регистрация нового пользователя              |
| `POST`   | `/token`           | 🔑 Получение JWT токена по логину и паролю      |
| `POST`   | `/refresh`         | ♻️ Обновление токенов по refresh_token     |
| `GET`    | `/urls`            | 📄 Получение всех отслеживаемых URL             |
| `POST`   | `/urls`            | ➕ Добавление нового URL в мониторинг           |
| `GET`    | `/urls/{id}`       | 🔍 Получение информации об URL по `id`          |
| `PATCH`  | `/urls/{id}`       | ⏱ Изменение интервала мониторинга              |
| `DELETE` | `/urls/{id}`       | 🗑 Удаление URL из мониторинга                  |
| `GET`    | `/history`         | 🕓 Получение истории проверок по `id` URL       |

---

### Регистрация нового пользователя 

| Путь         | Параметры                  |
|--------------|----------------------------|
| POST /register | `username`: string<br>`password`: string |


**Пример запроса:**
```json
{
  "username": "user99999",
  "password": "secure_password"
}
```

**Пример ответа при удачной регистрации:**
```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer"
}
```

### Получение JWT токена по логину и паролю

| Путь        | Параметры                  |
|-------------|----------------------------|
| POST /token | `username`: string<br>`password`: string |

**Пример запроса:**
```json
{
  "username": "exampleuser",
  "password": "securepassword"
}
```

**Пример ответа:**
```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer"
}
```

### Обновление токенов по refresh_token

| Путь         | Параметры                       | 
|--------------|----------------------------------|
| POST /refresh | `refresh_token`: string         |

**Пример запроса:**
```json
{
  "refresh_token": "jwt"
}
```

**Пример ответа:**
```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer"
}
```

### Получение всех отслеживаемых URL

| Путь         | Параметры                       | 
|--------------|----------------------------------|
| GET /urls | `Authorization`: string ( в заголовке )        |

---

### Добавление нового URL в мониторинг

| Путь       | Параметры  |     
|------------|------------|
| POST /urls | `Authorization`: string (в заголовке)<br>`url`: string<br>`interval`: integer |

**Пример запроса (POST):**
```json
{
  "url": "https://example.com",
  "interval": 10
}
```

### Получение информации об URL по id

| Путь            | Параметры      | 
|-----------------|----------------|
| GET /urls/{id}  | `id`: integer (в path)<br>`Authorization`: string (в заголовке) |


### Изменение интервала мониторинга

| Путь              | Параметры       |
|-------------------|-----------------|
| PATCH /urls/{id}  | `id`: integer (в path)<br>`Authorization`: string (в заголовке)<br>`interval`: integer |

**Пример запроса:**

**Тело запроса:**
```json
{
  "interval": 15
}
```

### Удаление URL из мониторинга

| Путь               | Параметры                                                   |
|--------------------|-------------------------------------------------------------|
| DELETE /urls/{id}  | `id`: integer (в path)<br>`Authorization`: string (в заголовке) |

### Получение истории проверок по id URL

| Путь         | Параметры                  |
|--------------|----------------------------|
| GET /history | `Authorization`: string (в заголовке)<br>`id`: integer/null<br>`limit`: integer/null (в теле) |

**Пример запроса:**


**Тело запроса:**
```json
{
  "id": 1,
  "limit": 10
}
```
