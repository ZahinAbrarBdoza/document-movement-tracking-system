# Document Movement Tracking System

A Django application for tracking document movement.

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create your environment file.

```powershell
Copy-Item .env.example .env
```

Update `.env` with your real `SECRET_KEY` and PostgreSQL database credentials.

4. Apply migrations.

```powershell
python manage.py migrate
```

5. Run the development server.

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## GitHub Notes

Do not commit `.env`, local virtual environments, SQLite databases, or uploaded media files. These are ignored by `.gitignore`.
