# ABOUT APP
## Versions
```shell
$ python3 --version  # v3.10.12
```

## Structure
```
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
```

# HOW TO USE

## Setup app (in venv)
```shell
$ bash setup.sh
```

## Run app (in venv)
```shell
$ bash run.sh
```

## Run test (in venv)

## Prettier / format code (in venv)
```shell
# $ python3 -m pip install virtualenv
# $ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ black . -S # (-S for keeping the single quote)
```

# NOTE
## Before commit
```shell
python manage.py makemigrations
python manage.py migrate
```

## Troubleshoot
- Some data schema changes -> force 'db.sqlite3' to update the initial default data. If we don't want, one of simple ways for this small projetc is to reset 'db.sqlite3'.