## Технологии

- Python 3.11
- Django 4.2.3
- Django REST framework 3.14.0
- JavaScript

## Запуск проекта из образов с Docker hub

Для запуска необходимо на создать папку проекта `foodgram` и перейти в нее:

```bash
mkdir foodgram
cd foodgram
```

В папку проекта скачиваем файл `docker-compose.production.yml` и запускаем его:

```bash
sudo docker compose -f docker-compose.production.yml up
```

Произойдет скачивание образов, создание и включение контейнеров, создание томов и сети.


## Запуск проекта с GitHub

Клонируем себе репозиторий: 

```bash 
git clone git@github.com:AndreiKlevtsov/foodgram-project-react.git
```

Выполняем запуск:

```bash
cd foodgram-project-react/nginx
docker compose -f docker-compose.yml up
```

## После запуска проекта:

Далее необходимо выполнить сбор статистики и миграции бэкенда. Статистика фронтенда собирается во время запуска контейнера, после чего он останавливается. 

```bash
docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py migrate

docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py collectstatic

docker compose -f [имя-файла-docker-compose.yml] exec backend cp -r /app/collected_static/. /backend_static/static/
```

И далее проект доступен на: 

```
http://localhost:8080/
```

## Остановка контейнеров

В терминале, где запущены: **Ctrl+С**, или в новом терминале:

```bash
docker compose -f docker-compose.yml down
```

# Данные для второй проверки

## ip и домен сервера:
#### 158.160.69.243

https://foodgramklevtsov.duckdns.org/

## Суперюзер: 
#### email = a@d.mn 
#### pass = admin12345678

