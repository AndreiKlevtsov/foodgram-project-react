# Foodgram

![workflow](https://github.com/AndreiKlevtsov/foodgram-project-react/actions/workflows/main.yml/badge.svg/)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Tecnhologies

- Python 3.11
- Django 4.2.3
- Django REST framework 3.14
- Nginx
- Docker
- Postgres



Сервис Foodgram реализован для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone git@github.com:AndreiKlevtsov/foodgram-project-react.git
```
## Для работы с удаленным сервером:
* Выполните вход на свой удаленный сервер

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Локально отредактируйте файл gateway/nginx.conf и в строке server_name впишите свой IP и/или доменное имя.
* Скопируйте файлы docker-compose.yml и nginx.conf из директории gateway на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

* Cоздайте .env файл и впишите:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<name_postgres>
DB_USER=<user+postgres>
DB_PASSWORD=<password_postgres>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<secret key проекта django>
```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<name_postgres>
DB_USER=<user+postgres>
DB_PASSWORD=<password_postgres>
DB_HOST=<db>
DB_PORT=<5432>
    
DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>
    
SECRET_KEY=<secret key проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
``` 
  
* На сервере соберите docker-compose:
```
sudo docker-compose up -d --build
```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
- Соберите статические файлы:
```
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic --noinput
   ```
- Примените миграции:
```
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate --noinput
   ```
- Загрузите ингридиенты  в базу данных (необязательно):  
*Если файл не указывать, по умолчанию выберется ingredients.json*
```
sudo docker compose -f docker-compose.yml exec backend python manage.py shell
from foodgram.models import Ingredient
>>> from core.import_data import create_models
>>> create_models('./data/ingredients.json', Ingredient)
   ```
- Создать суперпользователя Django:
```
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
   ```
- Проект будет доступен по вашему IP

