### **Учебный проект api\_yamdb**
**Описание Infra\_sp2 сборка образов и контейнера Docker
Технологии Python 3.7 Django 2.2.26**
--------------------------------------------------------
### **Для сборки образа**
docker-compose up
### **Выполнить миграции**
docker-compose exec web python manage.py migrate
### **Создать суперпользователя**
docker-compose exec web python manage.py createsuperuser
### **Собрать статику**
docker-compose exec web python manage.py collectstatic --no-input

Автор Дмитрий
