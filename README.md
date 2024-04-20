# Как запустить проект?

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Roman821/yp_stt_bot.git
cd yp_stt_bot
```

### 2. Создайте виртуальное окружение

#### С помощью [pipenv](https://pipenv.pypa.io/en/latest/):

```bash
pip install --user pipenv
pipenv shell  # create and activate
```

#### Или классическим методом:

```bash
python -m venv .venv  # create
.venv\Scripts\activate.bat  # activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Установите переменные окружения (environment variables)

Создайте файл `.env`, это должно выглядеть так: `yp_stt_bot/.env`. После скопируйте это в `.env`

```dotenv
BOT_TOKEN=<your_bot_token>
DB_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
STT_API_KEY=<your_stt_api_key>
STT_FOLDER_ID=<your_stt_folder_id>
```
_**Не забудьте поменять значения на свои! (поставьте их после "=")**_

#### Больше о переменных:
BOT_TOKEN - [токен телеграм бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)<br>
DB_URL - [url базы данных](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) sqlalchemy<br>
STT_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
STT_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit

### 5. Запустите проект

```bash
python main.py
```

# Продакшен настройка

### 1. Установите [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 2. Установите [docker](https://docs.docker.com/engine/install/)

### 3. Установите [docker compose plugin](https://docs.docker.com/compose/install/linux/)

### 4. Клонируйте репозиторий

```bash
git clone https://github.com/Roman821/yp_stt_bot.git
cd yp_stt_bot
```

### 5. Установите переменные окружения (environment variables)

Создайте файл `.env`, это должно выглядеть так: `yp_stt_bot/.env`. После скопируйте это в `.env`

```dotenv
BOT_TOKEN=<your_bot_token>
DB_URL=postgresql://<username>:<password>@postgres:5432/<database_name>
STT_API_KEY=<your_stt_api_key>
STT_FOLDER_ID=<your_stt_folder_id>

# docker compose section
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database_name>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata
```
_**Не забудьте поменять значения на свои! (поставьте их после "=")**_

#### Больше о переменных:
BOT_TOKEN - [токен телеграм бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)<br>
DB_URL - [url базы данных](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) sqlalchemy<br>
STT_API_KEY - [API ключ](https://cloud.yandex.ru/ru/docs/iam/concepts/authorization/api-key) для использования Yandex SpeechKit<br>
STT_FOLDER_ID - [folder id](https://cloud.yandex.ru/ru/docs/resource-manager/operations/folder/get-id) для использования Yandex SpeechKit<br>

POSTGRES_USER - [POSTGRES_USER](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_PASSWORD - [POSTGRES_PASSWORD](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_DB - [POSTGRES_DB](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_HOST - [POSTGRES_HOST](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_PORT - [POSTGRES_PORT](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
PGDATA - [PGDATA](https://hub.docker.com/_/postgres) стандартная переменная окружения docker

### 6. Запустите docker compose

```bash
docker compose up -d
```

### 7. После успешного запуска проверьте сервер

```bash
docker compose logs -f
```


# Дополнительные возможности настройки

Помимо обязательных переменных окружения, есть опциональные, расширяющие возможности конфигурации проекта.
Ниже представлены эти переменные с типизацией и значениями по умолчанию
(несмотря на то, что представлен код на python, переменные окружения должны устанавливаться из файла `.env`).

```python
SECONDS_BLOCKS_LIMIT_BY_USER: int = 25  # лимит блоков секунд на пользователя
REQUEST_MAX_SECONDS: int = 30  # лимит секунд на один запрос в STT сервис
STT_SECONDS_IN_BLOCK: int = 15  # количество секунд в блоке секунд (тарификация происходит по блокам секунд)
STT_URL: str = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'  # url STT сервиса
STT_LANGUAGE: str = 'ru-RU'  # язык распознавания текста
```
