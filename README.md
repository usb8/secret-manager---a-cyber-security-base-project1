# ABOUT APP
## Introduction
Secret Manager is a basic web application, built on the Django framework that helps users safely store sensitive information, such as passwords and secret keys. It should be noted that learning practical security is the main purpose of this app. Therefore, its design intentionally includes five common flaws (in [OWASP Top Ten vulnerabilities 2017](https://owasp.org/www-project-top-ten/)) with fixes. Naturally, it has a simple structure focusing on the backend to show visitors how to attack and defend in practice in the easiest way.

## Versions
```shell
$ python3 --version  # v3.10.12
```

## Structure
- Prerequisite: understanding of Django project structure and how to create a Django app 
```
cyber-security-prj1/
├── (.venv/)
├── attack_files/       - Contains attack files
├── project1/
│   ├── asgi.py
│   ├── settings.py     - Django project configuration
│   ├── urls.py
│   └── wsgi.py
├── screenshots/        - Contains demo photos of flaws before and after fixing
├── secret_manager/
│   ├── templates/      - Contains HTML file
│   ├── models.py       - Data model for secret management
│   ├── urls.py         - URL routing for secret management application
│   ├── views.py        - Logical handling functions for HTTP requests
│   └── static/
│       └── style.css
├── manage.py
└── (db.sqlite3)
```

# HOW TO USE

## Setup app (in venv)
```shell
$ python3 --version  # This command should work first. 'python3' command is recommended instead of 'python'.
$ bash setup.sh
```

## Run app (in venv)
```shell
$ bash run.sh
# Accounts can be used for demo:
  # Username: alice, Pass: AlicePassword123!
  # Username: bob, Pass: BobPassword123!
# List urls for demo are mentioned in the Structure above (./secret_manager/urls.py)
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
## Before commit (for updating the database schema if needed)
```shell
python manage.py makemigrations
python manage.py migrate
```

## How to open SQLite file e.g. db.sqlite3
1. Download : Visit the official [DB Browser for SQLite website](https://sqlitebrowser.org/) and download the version that fits your operating system (Windows, macOS, or Linux).
2. Setting
3. Open file
  - Click the `Open Database` button in the upper left corner.
  - Browse to the location of the `db.sqlite3` file on your laptop and select it.
  - Once opened, you can:
    - View the data tables in the `Database Structure` tab .
    - Execute the SQL query in the `Execute SQL` tab .
    - View or edit data in the `Browse Data` tab .

## How to create a pickle file
```shell
python3 attack_files/exploit.py # python attack_files/exploit.py
# Then a new malicious.pickle file appears in folder attack_files/.
```