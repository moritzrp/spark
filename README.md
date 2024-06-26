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

Spark connects to a Postgres database. You can host your own
for development via docker or docker-compose.

```bash
docker compose up -d
```

This will start Postgres and listen on port 5432.

### Start server

```bash
python spark/manage.py runserver
```

### Run tests

```bash
python spark/manage.py test spark
```
