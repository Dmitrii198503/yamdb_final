**### \*\*Учебный проект api\\_yamdb\*\***

\*\*Описание Yamdb\_final CI CD проекта

Технологии Python 3.7 Django 2.2.26\*\*

**--------------------------------------------------------**

https://github.com/Dmitrii198503/yamdb\_final/actions/workflows/yamdb\_workflow/badge.svg

Адрес сайта

http://51.250.28.207/redoc/

Пример запроса

http://51.250.28.207/api/v1/titles/

Описание

Сайт является - базой отзывов о фильмах, книгах и музыке. 

Пользователи могут оставлять рецензии на произведения, а также комментировать эти рецензии. 

Администрация добавляет новые произведения и категории (книга, фильм, музыка и т.д.).

Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), 

контейнер проекта django + gunicorn и контейнер nginx

Как запустить

Необходимое ПО

Docker: https://www.docker.com/get-started

Docker-compose: https://docs.docker.com/compose/install/

Инструкция по запуску

Для запуска необходимо из ввести команду:

sudo docker-compose up -d --build

Затем узнать id контейнера, для этого вводим

sudo docker container ls

В ответ получаем примерно следующее

CONTAINER ID   IMAGE                     COMMAND                  CREATED         STATUS         PORTS                    NAMES

ab8cb8741e4a   nginx:1.19.0              "/docker-entrypoint.…"   7 minutes ago   Up 2 minutes   0.0.0.0:80->80/tcp       dmitrii\_nginx\_1

f78cc8f246fb   dmitrii031985/yamdb:latest   "/bin/sh -c 'gunicor…"   7 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp   dmitrii\_web\_1

a68243a0a5e2   postgres:12.4             "docker-entrypoint.s…"   7 minutes ago   Up 2 minutes   5432/tcp                 dmitrii\_db\_1

Нас интересует контейнер dmitrii\_web\_1, заходим в него командой

docker exec -it <CONTAINER ID> sh

И делаем миграцию БД, создаем суперюзера и сбор статики

python manage.py migrate

python manage.py createsuperuser

python manage.py collectstatic

При желании можно загрузить тестовую бд с контентом

python manage.py loaddata fixtures.json

Как пользоваться

После запуска проекта, подробную инструкцию можно будет посмотреть по адресу http://0.0.0.0/redoc/

Автор

Дмитрий Голубцов - https://github.com/Dmitrii198503
