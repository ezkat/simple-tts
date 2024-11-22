# Simple Django TTS Request API
[![simple-tts](https://github.com/ezkat/simple-tts/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/ezkat/simple-tts/actions/workflows/main.yml)

A RESTful API for managing TTS conversion requests.
Project is built with Django and DRF.
While the actual TTS generation is not implemented, the system simulates it and generates dummy files for demonstration purposes.


### Features
- Authentication
    - Token-based authentication
    - Only authenticated users can access and manage their requests.

- API operations
    - CRUD operations for TTS request.
    - Simulated TTS generation process.


## Setup
- Prerequisites
    - Python 3.10 or later
    - pip
    - virtualenv

- Installation
    1. Clone the repository
        ```
        git clone https://github.com/ezkat/simple-tts
        cd simple-tts
        ```
    2. Setup python virtualenv
        ```
        pip install virtualenv
        python -m virtualenv venv
        source venv/bin/activate
        ```
    3. Install dependencies
        ```
        pip install -r requirements.txt
        ```
    4. \(Optional\) Setup environment variables by creating .env file in the root directory and configure it as needed.
        ```
        # .env example
        DEBUG=True
        SECRET_KEY=123456
        ALLOWED_HOSTS=*
        MEDIA_URL=/media/
        MEDIA_ROOT=media/
        ```
    5. Apply migrations and collect statics
        ```
        python manage.py migrate
        python manage.py collectstatic
        ```
    6. Create a superuser to access admin panel
        ```
        python manage.py createsuperuser
        ```
    7. Start development server
        ```
        python manage.py runserver
        ```

## Environment values
```
DEBUG: bool
ALLOWED_HOSTS: list
INTERNAL_IPS: list
MEDIA_ROOT: Path
STATIC_ROOT: Path
MEDIA_URL: str
STATIC_URL: str
USE_I18N: bool
USE_TZ: bool
TIME_ZONE: str
LANGUAGE_CODE: str
DISABLE_SERVER_SIDE_CURSORS: bool
```

## Testing
- Run tests and view a coverage report
    ```
    coverage run manage.py test
    coverage report
    ```

## API Endpoints
### Authentication
- Request a new token:
    - POST /api/v1/auth/token/
    - Example:
        ```
        curl -X POST http://localhost:8000/api/v1/auth/token/ \
            -H "Content-Type: application/json" \
            -d '{"username": "api_user", "password": "123"}'
        ```
    - Returns: access token, refresh token
- Refreshing a token:
    - POST /api/v1/auth/token/refresh/
    - Example:
        ```
        curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
            -H "Content-Type: application/json" \
            -d '{"refresh": "refresh_token"}'
        ```
    - Returns: access token

### Conversion requests
- Get conversion requests:
    - GET /api/v1/conversion_requests/
    - Filters:
        - status:
            - values: COMPLETED, FAILED
    - Example:
        ```
        curl -X GET http://localhost:8000/api/v1/conversion_requests/?status=COMPLETED \
            -H "Authorization: Bearer access_token"
        ```
- Create a new TTS conversion request:
    - POST /api/v1/conversion_requests/
    - Example:
        ```
        curl -X POST http://localhost:8000/api/v1/conversion_requests/ \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer access_token" \
            -d '{"text": "Example text"}'
        ```
- Retrieve a conversion request:
    - GET /api/v1/conversion_requests/123/
    - Example:
        ```
        curl -X GET http://localhost:8000/api/v1/conversion_requests/123/ \
            -H "Authorization: Bearer access_token"
        ```
- Update a TTS conversion request:
    - PATCH /api/v1/conversion_requests/123/
    - Example:
        ```
        curl -X PATCH http://localhost:8000/api/v1/conversion_requests/123/ \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer access_token" \
            -d '{"text": "Updated example text"}'
        ```
- Delete a TTS conversion request:
    - DELETE /api/v1/conversion_requests/123/
    - Example:
        ```
        curl -X DELETE http://localhost:8000/api/v1/conversion_requests/123/ \
            -H "Authorization: Bearer access_token"
        ```



### Assumptions and design decisions
1. Simulated TTS generation
    - `output` field is a `FileField` that saves a dummy files for simulating the TTS generation process. Instead of saving the file, better practice would be sending audio stream back.
2. Error simulation
    - Added a random chance of failing the generation simulation
3. Text validation
    - Django and DRF already provide a broad range of automatic validation, but I added a simple html escape and unprintable characters strip validation.
4. Environment values
5. Simple query result filtering with status field
