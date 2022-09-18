[![yamdb-final-app workflow](https://github.com/agatma/yamdb_final/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/agatma/yamdb_final/actions/workflows/main.yml)

# Тестовое задание в ШБР Яндекса

REST API сервис, который позволяет пользователям загружать и обновляет информацию о файлах и папках
1. Пользователь загружает и структурирует файлы в предложенном ему облачном пространстве.
2. Пользователь может скачивать файлы и фиксировать историю их изменений.

## Стек технологий
- проект написан на Python с использованием Django REST Framework
- библиотека django-filter - фильтрация запросов
- базы данны - postgresql
- автоматическое развертывание проекта - Docker, docker-compose

## Запуск на локальном компьютере с помощью Docker
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта (на примере Linux)

- Склонируйте этот репозиторий в рабочую папку `git clone https://github.com/agatma/api_yandex_disk`
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
- Перейдите в папку infra/
- Запустите docker-compose командой `sudo docker-compose up -d --build`
- Создадутся три контейнера: web (приложение), postgres, nginx
- Накатите миграции `sudo docker-compose exec web python manage.py migrate`
- Соберите статику командой `sudo docker-compose exec web python manage.py collectstatic --no-input`
- Создайте суперпользователя Django `sudo docker-compose exec web python manage.py createsuperuser --username admin --email 'admin@yamdb.com'`
- Загрузите данные в базу данных при необходимости `sudo docker-compose exec web python manage.py loaddata data/fixtures.json`
## Запуск на удаленном сервере
Для запуска проекта на удаленном сервере необходимо:
- Откройте папку infra/
- скопировать на сервер файлы `docker-compose.yaml`, `.env` и папку `nginx` командами:
```
scp docker-compose.yaml  <user>@<server-ip>:
scp .env <user>@<server-ip>:
scp -r nginx/ <user>@<server-ip>:
```

- создать переменные окружения в разделе `secrets` настроек текущего репозитория:
```
DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USERNAME # Логин от Docker Hub
HOST # Публичный ip адрес сервера
USER # Пользователь зарегистрированный на сервере
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ
TELEGRAM_TO # ID телеграм-аккаунта
TELEGRAM_TOKEN # Токен бота
```

### После каждого обновления репозитория (`git push`) будет происходить:
1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория api_yandex_disk
2. Сборка и доставка докер-образов на Docker Hub.
3. Автоматический деплой.
4. Отправка уведомления в Telegram.

## Запуск на локальном компьютере без Docker

1) Клонируйте репозитроий с проектом
2) В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости:
```
python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt
```
3) Выполните миграции:
```
python manage.py migrate
```
4) Cоздайте суперпользователя:
```
python manage.py createsuperuser
```
5) Запустите сервер:
```
python manage.py runserver
```
__________________________________

Ваш проект запустился на http://127.0.0.1:8000/

