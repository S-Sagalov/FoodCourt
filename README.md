![status](https://github.com/S-Sagalov/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Технологии, используемые в проекте:

`Python` `Django` `Django Rest Framework` `Docker` `NGINX` `PostgreSQL` `Yandex Cloud`

# Foodgram
Сервис для публикации рецептов.
Проект временно доступен для просмотра по [ссылке](158.160.3.131)


## Запуск проекта на сервере

1)Склонировать репозиторий:

```
git clone https://github.com/S-sagalov/yamdb_final.git
```

2)Выполнить вход на свой сервер

3)Установить docker на сервер:

```
sudo apt install docker.io
```

4)Установить docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

5)Скопировать на сервер файлы docker-compose.yml и nginx.conf из папки infra


6)Запустить docker-compose:

```
docker-compose up -d --build
```

7)Собрать файлы статики, создать и выполнить миграции:

```
docker-compose exec web python3 manage.py makemigrations
```
```
docker-compose exec web python3 manage.py migrate
```
```
docker-compose exec web python3 manage.py collectstatic --no-input
```
