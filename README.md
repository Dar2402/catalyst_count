# Catalyst Count Project Setup

Welcome to the Django project! This README will guide you through setting up the project on your local machine, including creating a virtual environment, installing dependencies, and running the server. Let's get started!

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
   - [1. Clone the Repository](#1-clone-the-repository)
   - [2. Create and Activate Virtual Environment](#2-create-and-activate-virtual-environment)
   - [3. Install Dependencies](#3-install-dependencies)
   - [4. Update Database Credentials](#4-update-database-credentials)
   - [5. Download Test Data](#5-download-test-data)
   - [6. Run Migrations](#6-run-migrations)
   - [7. Create Superuser](#7-create-superuser)
3. [Start the Development Server](#start-the-development-server)
4. [Additional Commands](#additional-commands)

## Prerequisites

- Python 3.8 or later
- Git
- Virtual Environment Tools: `venv` or `virtualenv`
- PostgreSQL or other supported databases (optional, based on settings)

## Project Setup

### 1. Clone the Repository

First, clone the project repository from GitHub:

```bash
git clone https://github.com/Dar2402/catalyst_count.git
cd catalyst_count
```

### 2. Create and Activate Virtual Environment

You need to create a virtual environment to isolate project dependencies.

#### Linux / macOS:

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

#### Windows:

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is active, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Update Database Credentials

Open the `settings.py` file and update the database configuration if needed. You can leave it as is if you're using the default SQLite configuration.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or use 'django.db.backends.sqlite3' for default
        'NAME': '<your-database-name>',
        'USER': '<your-database-user>',
        'PASSWORD': '<your-database-password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

> **Note:** Make sure PostgreSQL is installed and running if you're using it.

### 5. Download Test Data

Download the dataset from the following link and upload it to your database:

[Download the test dataset](https://www.dropbox.com/scl/fi/r97699phgl1xbjzlenfgi/free-7-million-company-dataset.zip?rlkey=9xi6i2pl0kv4giifaae9sshj0&dl=0)

Follow instructions for loading the dataset into your database.

### 6. Run Migrations

Run the following commands to apply the migrations and set up your database schema:

```bash
python manage.py migrate
```

### 7. Create Superuser

You will need a superuser to access the Django admin panel. Create one by running:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up a username, email, and password.

## Start the Development Server

To start the Django development server, run:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to view the project.

## Additional Commands

- **To deactivate the virtual environment:**

  ```bash
  deactivate
  ```

- **To install new dependencies:**

  If you add new dependencies, you can update the `requirements.txt` file using:

  ```bash
  pip freeze > requirements.txt
  ```

- **To check for any issues with your Django setup:**

  ```bash
  python manage.py check
  ```

---
