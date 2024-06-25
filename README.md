# Spark

Spark is used to demonstrate Django in combination with the GitOps approach.

I'm also using it to test new tools and principles that improve the
workflow and development experience.

## Development

After cloning the repository, you can set up the environment:

```bash
# Create your virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hook
pre-commit install
```

### Start services

Spark is meant to run in a container. This can also be used for development.
When you update the code on your local machine, the development server
will reload and reflect those changes.

Spark connects to a Postgres database. Postgres will run as a separate container.

To start both services, you can use docker compose:

```bash
docker compose up -d
```

This will start Spark and Postgres and listen on port 8000 and 5432 respectively.
You can adjust the port mappings to your liking in the `docker-compose.yml` file.

### Start server

```bash
python spark/manage.py runserver
```

### Run tests

```bash
python spark/manage.py test spark
```
