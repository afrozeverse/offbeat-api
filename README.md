# Offbeat API

**Offbeat API** is the backend service for *Offbeat*, a travel discovery platform that suggests **offbeat and lesser-known places to visit**. This Django REST API powers the core data and logic used by frontend clients and mobile applications.

---

##  Overview

Offbeat API handles:
- User authentication (signup, login)
- Place discovery endpoints
- Reviews & ratings for places
- Search and filter features
- Secure request handling

It is built with **Django** and **Django REST Framework** and designed for deployment on platforms such as **Render**.

---

##  Tech Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Django |
| API Toolkit | Django REST Framework |
| Database (Local) | SQLite |
| Deployment | Render |
| Env Management | python-dotenv |

---

##  Features

✔ RESTful APIs for users and places  
✔ Structured app modules (`places`, `reviews`, `users`, `services`)   
✔ Authentication and permissions  
✔ Search and filtering endpoints  
✔ Environment variable support for security

---

##  Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/afrozeverse/offbeat-api.git
cd offbeat-api

2️⃣ Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt
🔧 Setup Environment Variables
Create a .env file in the project root:

SECRET_KEY=your_django_secret_key
DEBUG=True
IMPORTANT: Do not commit .env to GitHub.

🗄️ Database
Make migrations and migrate:

python manage.py makemigrations
python manage.py migrate
🧪 Run Server Locally
python manage.py runserver
Visit: http://127.0.0.1:8000/

🚀 Deployment on Render
Push this repo to GitHub (already done).

Create a new Web Service in Render.

Connect the GitHub repo.

Add environment variables in Render dashboard:

SECRET_KEY
DEBUG=False
Render will auto-deploy.

🪪 Requirements
Example of requirements.txt:

Django
djangorestframework
django-cors-headers
python-dotenv
Directory structure includes:

offbeat/, places/, reviews/, services/, users/

manage.py

.gitignore

requirements.txt 

📚 API Documentation
You can add automated API docs (Swagger / OpenAPI) in future to support frontend developers and testers.

🤝 Contributing
Feel free to:

Add new endpoints

Improve models or serializers

Add tests

Pull requests are welcome!

🔐 Notes
SECRET_KEY and other secrets must never be in version control.

For deployment, ensure DEBUG=False.

## 🔗 API Endpoints

Below are the main API endpoints provided by this backend.

### 🔐 Authentication

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login user and return tokens |

---

### 👤 User

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/profile/` | Get logged-in user profile |

> Authentication required for protected routes.

---

### 🗺 Places

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/places/` | Get list of offbeat places |
| GET | `/api/places/<id>/` | Get details of a place |

---

### ⭐ Reviews

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/reviews/` | Add a review |
| GET | `/api/reviews/<place_id>/` | Get reviews for a place |

### Example Request

**GET /api/places/**

Response:
```json
[
  {
    "id": 1,
    "name": "Dzukou Valley",
    "location": "Nagaland",
    "description": "A peaceful offbeat destination"
  }
]

📜 License
This repository is open-source and available under the terms in the repository. Feel free to reuse and build on it!
