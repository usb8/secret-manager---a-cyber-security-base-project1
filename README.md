
## Before commit
```shell
python manage.py makemigrations
python manage.py migrate
```

## Troubleshoot
- Some data schema changes -> force 'db.sqlite3' to update the initial default data. If we don't want, one of simple ways for this small projetc is to reset 'db.sqlite3'.