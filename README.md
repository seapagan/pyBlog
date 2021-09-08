# Django-based Blogging engine

This is work in progress to write a blogging Engine in Django for my own use,
and release as OSS when it reaches that level.

This README is very basic and will be updated as more functionality is coded
into the project.

## Development

From the root of the checked out repository.

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Migrate the database

You will need to adjust the database settings to your own needs, the application
defaults to using a file-based `SQLite` database.

```bash
python manage.py migrate
```

### Run the Development server

The application defaults to **Production** mode unless the `DEBUG` variable is set
to 1

```bash
DEBUG=1 python manage.py runserver
```

You can now access the application in your browser at `http://localhost:8000`
