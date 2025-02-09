# File Upload Service

A Django-based service for handling large file uploads (4GB-8GB) efficiently with support for multiple concurrent uploads.

## Features

- RESTful API for file uploads and listing
- Support for large files (4GB-8GB)
- Concurrent upload handling
- File metadata and storage location management
- Docker-based deployment
- Scalable client testing

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd file_upload_service
```

2. Build and start the services:
```bash
docker-compose build
docker-compose up -d
```

3. Run migrations:
```bash
docker-compose exec django python manage.py migrate
```

## Testing

### Running the Test Suite

```bash
docker-compose exec django pytest
```

### Load Testing with Multiple Clients

To test the system with multiple concurrent uploads:

```bash
docker-compose up --scale client=6 -d
```

This will start 6 client containers, each generating and uploading a random file between 4GB and 8GB.

## API Endpoints

### Upload File
- **URL**: `/api/v1/files/upload/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: The file to upload
  - `metadata`: JSON string containing:
    - `intended_path`: Target storage location
    - `description`: File description

### List Files
- **URL**: `/api/v1/files/`
- **Method**: `GET`
- **Response**: List of uploaded files with metadata

## Project Structure

```
.
├── compose/                 # Docker compose configuration
├── config/                  # Django settings
├── file_uploads/           # Main application
├── requirements/           # Python dependencies
└── tests/                 # Test suite
```

## Development

1. Make sure Docker and Docker Compose are installed
2. Build the development environment: `docker-compose build`
3. Start the services: `docker-compose up -d`
4. Run migrations: `docker-compose exec django python manage.py migrate`
5. Access the API at `http://localhost:8000/api/v1/`

## License

MIT License

# file-upload-service

FileUpload

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy file_upload_service

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd file_upload_service
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd file_upload_service
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd file_upload_service
celery -A config.celery_app worker -B -l info
```

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
