
## Before commit
```shell
python manage.py makemigrations
python manage.py migrate
```

## Troubleshoot
- Some data schema changes -> force 'db.sqlite3' to update the initial default data. If we don't want, one of simple ways for this small projetc is to reset 'db.sqlite3'.

## Structure
cyber-security-prj1/
├── project1/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── secret_manager/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── secrets.html
│   │   ├── secret_detail.html
│   │   └── create_secret.html
│   └── static/
│       └── style.css
├── manage.py
└── db.sqlite3