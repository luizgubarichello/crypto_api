# Crypto API Challenge

A simple REST API for generating valid cryptocurrency addresses and displaying them. Specifically, the API should provide three endpoints, as follows:

    1. Generate Address: The core functionality of the API is to take a cryptocurrency as input and return a valid address for that currency as output.

    2. List Address: The List endpoint takes no input and returns a list of all the addresses generated so far.

    3. Retrieve Address: The Retrieve endpoint takes an ID, and returns the corresponding address as stored in the database.

## Stack used

- Python
- Django
- Django REST Framework
- Celery
- Redis
- Docker

## How to install and use

To install and use this project, follow the steps:

### Via Docker

1. Execute the command `git config --global core.autocrlf false`

2. Clone this repo

3. Execute the command `docker-compose up` and wait for the process to finish (finishes when the web server initializes)

4. Go to local step 7

### Local (if in Windows use WSL)

1. Clone this repo

2. Certify that you have Redis installed and running

3. Install project dependencies:
    - `pip3 install -r requirements.txt`

4. Migrate the DB:
    - `python3 manage.py makemigrations`
    - `python3 manage.py migrate`

5. Run the live server:
    - `python3 manage.py runserver`

6. Start the celery worker:
    - `celery -A crypto_api worker -l info`

7. The app has the following endpoints:
    - GET `/docs/swagger/` for docs
    - GET `/api/list/` for the list of addresses generated so far
    - GET `/api/retrieve/<pk>/` to retrieve a specific ID
    - POST `/api/generate/` to generate a new address

