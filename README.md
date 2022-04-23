# Учебный проект api_yamdb
## _Описание Yamdb_final CI CD проекта Технологии Python 3.7 Django 2.2.26_

![yamdb_workflow](https://github.com/Dmitrii198503/yamdb_final/actions/workflows/yamdb_workflow/badge.svg)

Адрес сайта http://51.250.28.207/redoc/

- Пример запроса
- http://51.250.28.207/api/v1/titles/
- ✨Magic ✨

## Описание

- Сайт является - базой отзывов о фильмах, книгах и музыке.
- Пользователи могут оставлять рецензии на произведения, а также комментировать эти рецензии.
- Администрация добавляет новые произведения и категории (книга, фильм, музыка и т.д.).
- Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), 
контейнер проекта django + gunicorn и контейнер nginx


Необходимое ПО

Docker: https://www.docker.com/get-started

Docker-compose: https://docs.docker.com/compose/install/

> Посмотреть запущенные контейнеры sudo container ls
контейнер dmitrii_web_1, заходим в него командой
docker exec -it <CONTAINER ID> sh
И делаем миграцию БД, создаем суперюзера и сбор статики
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
При желании можно загрузить тестовую бд с контентом
python manage.py loaddata fixtures.json


## Как пользоваться

После запуска проекта, подробную инструкцию можно будет посмотреть по адресу http://<HOST>/redoc/



## Автор

Дмитрий Голубцов - https://github.com/Dmitrii198503

