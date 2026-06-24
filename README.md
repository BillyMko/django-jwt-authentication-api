# Django JWT Authentication API

## Project Overview

This project is a secure authentication API built using Django, Django REST Framework, and JWT authentication.

## Features

- User registration
- Email verification
- Log in using email and password
- JWT login (access + refresh)
- Password reset via email
- Role-based permissions (admin, user, premium)

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite3
- python-dotenv


## API Endpoints

### Authentication

- POST /api/register/
- POST /api/login/
- POST /api/logout/
- POST /api/token/refresh/
---

### Email Verification

- GET /api/verify-email/

---

### Profile

- GET /api/profile/
- PATCH /api/testprofile/

---

### Password Reset

- POST /api/password-reset/request/
- POST /api/password-reset/confirm/

---

### Admin

- GET  /api/admin/users/
- PATCH  /api/admin/users/<id>/

---

## Project Notes

- Uses JWT authentication
- Email system currently supports logging mode
- Token blacklisting enabled for logout security
## To run Locally
git clone https://github.com/BillyMko/django-jwt-authentication-api.git

## Create Virtual Environment and Activate

python -m venv myenv

source myenv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Create superuser

python manage.py createsuperuser

## Run migrations and Start Development Server

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

## Environment Variables

Create a `.env` file in the project root and add:

```env
SECRET_KEY=django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost