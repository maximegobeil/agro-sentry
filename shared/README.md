# Django Shared Core

A Django reusable app providing shared functionality across multiple services, including a custom user model with email authentication.

## Features

- Custom User model using email for authentication
- Extended User fields (first_name, last_name, phone_number)
- Custom admin interface
- Phone number field support

## Installation

1. Add the package to your project:

```bash
pip install -e path/to/django-shared-core
```

2. Add 'core' to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # add this
]
```

3. Add the custom user model to your settings:

```python
AUTH_USER_MODEL = 'core.CustomUser'
```

4. Run migrations:

```bash
python manage.py makemigrations core
python manage.py makemigrations
python manage.py migrate
```

## Development Setup

1. Clone the repository
2. Install development dependencies
3. Create and activate a virtual environment

## Available Models

### CustomUser

- email (used for authentication)
- first_name
- last_name
- phone_number
- is_active
- is_staff
- date_joined

## Forms

- CustomUserCreationForm: For creating new users
- CustomUserChangeForm: For modifying existing users

## Admin Interface

The package includes a custom admin interface for managing users with the following features:

- List display: email, first_name, last_name, is_staff, is_active
- Search fields: email, first_name, last_name
- Fieldsets for organized user management

## Requirements

- Django >= 5.1.6
- django-phonenumber-field[phonenumbers] >= 5.0.0
- asgiref >= 3.8.1
- sqlparse >= 0.5.3

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
