# Simple chat project

# Configure Local Development Environment
## Requirements
1. Python 3.10
2. Windows OS

## Steps
1. Create virtual environment: 
```bash
py -m venv venv
```

2. Activate virtual environment:
```bash
venv\Scripts\activate
```

3. Install all dependencies:
```bash
pip install -r requirements.txt 
```

4. Migrate all migrations:
```bash
python manage.py migrate 
```

5. Create admin user:
```bash
python manage.py createsuperuser
```

6. Launch tests:
```bash
python manage.py test
```

7. Launch server:
```bash
python manage.py runserver
```

After all manipulations you can access admin panel in browser by link:
```bash 
http://127.0.0.1:8000/admin
```
For using REST API, you can check Project APIs in browser list by link:
```bash 
http://127.0.0.1:8000/swagger

(Most REST APIs uses Bearer token, that you can get by url /auth/login/)
```
