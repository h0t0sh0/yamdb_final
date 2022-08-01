# Study project yamdb
### Description
The project is designed to create a database of creations with a system of reviews and ratings

### Technical stuff
- Python 3.7
- Django 2.2.19

### Steps for running in dev
- Go to the directory containing docker-compose.yaml
  ```cd infra```
- Run docker-compose to build the images and launch containers
  ```docker-compose up -d --build```
- Run migrations on the database to create the tables for the project
  ```docker-compose exec web python manage.py migrate```
- We need a superuser to manage and administer the project, you can create it with the command
  ```docker-compose exec web python manage.py createsuperuser```
- Let's collect the static files in a common nginx and django directory
  ```docker-compose exec web python manage.py collectstatic --no-input```
- File fixtures.json contains a set of test data, you can upload them to the project with the command
  ```docker-compose exec web python manage.py loaddata fixtures.json```
- Open http://localhost/admin/ in your browser and enjoy

### Example for .env file
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

# Author
Vitaly Ostashov
h0t0sh0@yandex.ru
