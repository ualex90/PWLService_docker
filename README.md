# PWLService
<h3>Запуск проекта</h3>

Для запуска проекта должен быть установлен docker engine.
Инструкция по установке: https://docs.docker.com/engine/install/<br/>
Для Ubuntu, дополнительно нужно установить docker-compose:

```bash
sudo apt install docker-compose
```

В корне проекта необходимо создать и заполнить файл .env:

```
# .env

DEBUG='on'
SECRET_KEY=

DATABASE_NAME='postgres'
DATABASE_USER='postgres'
DATABASE_PASSWORD='mysecretpassword'
DATABASE_HOST='db'

STRIPE_API_KEY=

EMAIL_HOST=
EMAIL_PORT=465
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_SSL='on'
```
Для первого запуска необходимо собрать образ контейнера. Для этого, находясь в корневой директории проекта
необходимо выполнить команду:

```bash
sudo docker-compose build
```

Для запуска проекта:

```bash
sudo docker-compose up
```

Веб приложение будет доступно по адресу: http://127.0.0.1:8000

<h3>Cоздание демонстрационных пользователей</h3>

Админ:
```bash
docker-compose exec app python3 manage.py ccsu 
```
Обычные пользователи и 1 из них модератор:
```bash
docker-compose exec app python3 manage.py ccusers 
```
При создании пользователей в консоль выведутся email, пароли и группы

<h3>Заполнение базы данных из фикстур</h3>

```bash
docker-compose exec app python3 manage.py loaddata fixtures/db.json
```

Администратор:
```
email = 'admin@sky.pro'
password = 'admin'
```
Пользователи:
```
ivanov@sky.pro - MODERATOR
petrov@sky.pro
sidorov@sky.pro

password - 123qwe
```
# PWLService_docker
