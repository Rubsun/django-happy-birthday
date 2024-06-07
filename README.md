# Django Happy Birthday

## Description
Django Happy Birthday - This is a Django project designed to send birthday notifications. The project uses Celery for asynchronous tasks and Redis as a message broker.

##Time
The time in the app is UTC + 0

## Requirements
- Python 3.10
- PostgreSQL
- Redis
- virtualenv

## Installation and configuration

### Step 1: Clone the repository
```bash
git clone https://github.com/Rubsun/django-happy-birthday
cd django_happy_birthday
```

### Step 2: Create a virtual environment and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Creating a PostgreSQL container
```bash
docker run -d --name app -p 5551:5432 -e POSTGRES_PASSWORD=123 -e POSTGRES_USER=app -e POSTGRES_DB=app  postgres
```
### Step 4: Make migrations and migrate
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
### Step 5: Start redis with worker and beat
```bash
sudo apt-get install redis-server
sudo service redis-server start
celery -A django_happy_birthday worker -l INFO
celery -A django_happy_birthday beat --loglevel=info
```

### Step 6 Launching the Django Server
```bash
python manage.py runserver
```
