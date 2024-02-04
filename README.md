![status](https://github.com/S-Sagalov/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# FoodCourt
Проект сайта-кулинарного блога, где пользователи могут публиковать свои рецепты, просматривать рецепты других людей, подписываться на любимых авторов, а так же формировать корзину покупок.

<details>
<summary>Запуск проекта на сервере</summary>

1) Клонировать репозиторий:

```
git clone git@github.com:S-Sagalov/FoodCourt.git
```

2) Выполнить вход на свой сервер

3) Установить docker на сервер:

```
sudo apt install docker.io
```

4) Установить docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

5) Скопировать на сервер файлы docker-compose.yml и nginx.conf из папки infra


6) Запустить docker-compose:

```
docker-compose up -d --build
```

7) Собрать файлы статики, создать и выполнить миграции:

```
docker-compose exec web python3 manage.py makemigrations
```
```
docker-compose exec web python3 manage.py migrate
```
```
docker-compose exec web python3 manage.py collectstatic --no-input
```
</details>

<details>
<summary>Запуск проекта локально</summary>

1) Клонировать репозиторий и перейти в папку "infra":

```
git clone git@github.com:S-Sagalov/ArtAppreciation.git
cd infra
```
2) Запустить сборку контейнеров:
```
docker-compose -up
```
3) Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

4) Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

5) Собрать файлы статики:

```
docker-compose exec web python3 manage.py collectstatic --no-input
```

6) Заполнить базу данными:

```
docker-compose exec web python manage.py loaddata fixtures.json 
```

</details>

<details>
<summary>Стек</summary>

- [![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/Django-2.2.19-blue?style=flat-square&logo=Django&logoColor=3776AB&labelColor=d0d0d0)](https://docs.djangoproject.com/en/4.2/releases/2.2.19/)
- [![DRF](https://img.shields.io/badge/DRF-3.12.4-blue?style=flat-square&logoColor=3776AB&labelColor=d0d0d0)](https://www.django-rest-framework.org/community/release-notes/#3124)
- [![DRFSimpleJWT](https://img.shields.io/badge/DRF_SimpleJWT-4.8.0-blue?style=flat-square&logoColor=3776AB&labelColor=d0d0d0)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [![Docker](https://img.shields.io/badge/Docker-blue?style=flat-square&logo=Docker&logoColor=3776AB&labelColor=d0d0d0)](https://www.docker.com/)
- [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?style=flat-square&logo=PostgreSQL&logoColor=3776AB&labelColor=d0d0d0)](https://www.postgresql.org/)
- [![PostgreSQL](https://img.shields.io/badge/NGINX-blue?style=flat-square&logo=NGINX&logoColor=3776AB&labelColor=d0d0d0)](https://nginx.org/)

</details>