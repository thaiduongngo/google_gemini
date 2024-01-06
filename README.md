# Prerequisites
### Install git client
*https://git-scm.com/downloads*
### Install python
*https://www.python.org/downloads/*
*(Python 3.11 is recommended)*
### Install PostgreSQL
*https://www.postgresql.org/download/*
### Install pgvector extension
*https://github.com/pgvector/pgvector*

# Clone project
```commandline
git clone https://github.com/thaiduongngo/google_gemini.git
```

# Create project virtual environment
Go to project home folder
```commandline
python -m venv venv
```
or 
```commandline
python3 -m venv venv
```
*https://docs.python.org/3/library/venv.html*

# Create .env file
At home folder, create a `.env` file and append the content into the file. You can copy `dotenv` to `.env` and 
inject corresponding values into the file.
```
GOOGLE_API_KEY={google_api_key}
APP_HOME={full_path_to_home_folder}
```
Register a Google account and create a Google API Key for Gemini here:\
*https://ai.google.dev/*

# Activate project
At home folder
* macOS: `source venv/bin/activate`
* Windows CMD: `venv\Scripts\activate.bat`
* Windows PS: `venv\Scripts\Activate.ps1`

# Install all Python packages
Make sure requirements.txt in the home folder
```commandline
pip install -e .
```

# Start RESTful API
```
gunicorn --workers={num_of_workers} --timeout=3600 --bind=0.0.0.0:{port_num} 'api.app:create_app()'
```
For example: 
```
gunicorn --workers=2 --timeout=3600 --bind=0.0.0.0:8081 'api.app:create_app()'
```

### Use Postman to test API
```
[POST] http://localhost:8081/api/chat

Payload:
{
    "text_message": "Các điều khoản loại trừ Pru vững chắc" 
}
```

# Start Jupyter Notebook
```commandline
jupyter notebook
```
