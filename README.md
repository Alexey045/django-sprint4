# Blogicum, sprint 3

A Django blog with user profiles, image uploads, scheduled and private posts, comments, pagination, account pages, and email files saved locally.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python blogicum\manage.py migrate
python blogicum\manage.py createsuperuser
python blogicum\manage.py runserver
```

Open http://127.0.0.1:8000/. Create categories and locations in `/admin/` before publishing posts.
