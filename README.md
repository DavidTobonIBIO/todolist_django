# To-Do List Web App using Django

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- pip

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DavidTobonIBIO/todolist_django.git
cd todolist_django
```

### 2. Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Requirements
```bash
pip install -r requirements.txt
```

Or you can install the dependencies manually:
```bash
pip install django
pip install django-crispy-forms
pip install crispy-bootstrap5
```

## Configuration
Run the following commands to set up the SQLite database:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the app
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`
