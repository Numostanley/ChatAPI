# ChatAPI

Installation

Clone the repository:

```
git clone https://github.com/Numostanley/ChatAPI.git
```

Enter the root directory.
```
cd ChatAPI
```

Create a virtual environment.
```
python -m venv venv
```

Activate the virtual environment.

On Windows:
```
venv\Scripts\activate
```

On macOS and Linux:
```
source venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Database Setup

Apply migrations:
```
python manage.py migrate
```

Create a superuser (for Django admin access):
```
python manage.py createsuperuser
```
Follow the prompts to create a superuser account.

Running the Project
```
python manage.py runserver
```
