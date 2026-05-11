# Django JWT Authentication API

## Project Overview

This project is a secure authentication API built using Django, Django REST Framework, and JWT authentication.

The API allows users to:

- Register accounts
- Log in using email and password
- Receive JWT access and refresh tokens
- Access protected route

This project was built to practice backend authentication, API security, token-based authentication, and deployment preparation on render.

## Technologies Used

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite3
- python-dotenv

## Authentication Flow

1. User registers using email, username, and password.
2. User logs in and receives:
   - Access token
   - Refresh token
3. Access token is used to access protected endpoint.
4. When access token expires, refresh token can be used to generate a new access token.

## API Endpoints

### Register User

POST `/api/register/`

Request Body:

```json
{
  "username": "sarah",
  "email": "sarah@gmail.com",
  "password": "sarah123"
}

```

Response:

```json
{
  "id": 1,
  "username": "sarah",
  "email": "sarah@gmail.com"
}

```
---
### Login

POST `/api/login/`

Request Body:

```json
{
  "email": "sarah@gmail.com",
  "password": "sarah123"
}

```

Response:

```json
{
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}

```
---

### Profile Endpoint

GET `/api/profile/`

Headers:

```text
Authorization: Bearer access_token_here

```
Response:

```json
{
  "id": 1,
  "username": "sarah",
  "email": "sarah@gmail.com"
}
```
## To run Locally
git clone https://github.com/BillyMko/django-jwt-authentication-api.git

## Create Virtual Environment and Activate

python -m venv myenv

source myenv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Run migrations and Start Development Server

python manage.py migrate

python manage.py runserver

## Environment Variables

Create a `.env` file in the project root and add:

```env
SECRET_KEY=django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost