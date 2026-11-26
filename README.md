# PromiseLane

PromiseLane is a Django web application for creating matrimonial profiles and
discovering compatible people. Members can manage their profiles, browse and
filter other profiles, and express interest in other members.

## Features

- Account registration, login, logout, and profile management
- Matrimonial profiles with education, occupation, location, and other details
- Profile browsing and filtering by gender, religion, city, and marital status
- Interest requests with sent, received, and response views
- Partner preferences, profile visibility controls, blocking, and profile reports
- Django admin interface

## Technology

- Python
- Django 6.1.3
- SQLite for local development
- Pillow for profile image uploads
- HTML, CSS, and JavaScript

## Local setup

Use a Python version supported by Django 6.1.3. From the project root, create
and activate a virtual environment, then install the application dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Django==6.1.3 Pillow==13.0.0
```

Apply database migrations and start the development server:

```powershell
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. The Django admin is available at
<http://127.0.0.1:8000/admin/>.

Run the automated tests with:

```powershell
python manage.py test
```

## Project layout

| Path | Purpose |
| --- | --- |
| `config/` | Django settings and project-level URL configuration |
| `authen/` | Account registration, authentication, and account profile |
| `user_profile/` | Matrimonial profile creation and editing |
| `dashboard/` | Member dashboard and profile discovery |
| `connections/` | Interests, partner preferences, blocking, and reporting |
| `templates/`, `static/` | Shared pages and static assets |
| `media/` | Local uploaded images and image assets |

## Before publishing or deploying

The current settings are for local development, not production. Before
deploying, move the Django `SECRET_KEY` out of source code and into a secure
environment variable, set `DEBUG` to `False`, configure `ALLOWED_HOSTS`, and
use a production-ready database and static/media file storage.

Before pushing this repository to a public remote, review the tracked
`db.sqlite3` and files under `media/profile/`. They may contain local database
records or uploaded profile photos; remove any private or personal data from
the repository. Do not commit virtual environments, caches, credentials, or
real user uploads.
