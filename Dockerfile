# docker hub image python:3.13-slim
FROM python:3.13-slim

# docker container inner folder
WORKDIR /app 

# debian package manager
# build-essential for compiling C extensions
# libpq-dev for PostgreSQL support
# rm -rf /var/lib/apt/lists/* to clean up apt cache
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pipfile for dependencies
# Pipfile.lock for exact versions
# --ignore-pipfile to use only the locked versions
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# migrations and static files
COPY . .
RUN pipenv run python manage.py makemigrations \
    && pipenv run python manage.py migrate \
    && pipenv run python manage.py collectstatic --noinput

# execute this command when docker run
CMD ["pipenv", "run", "gunicorn", "shopping.wsgi:application", "--bind", "0.0.0.0:8000"]