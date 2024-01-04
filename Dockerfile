FROM python:3.11.7-slim-bullseye

RUN mkdir -p /app/api
RUN mkdir -p /app/generative_ai

ENV APP_HOME='/app'

COPY ./api/__init__.py /app/api/
COPY ./api/app.py /app/api/
COPY ./api/service.py /app/api/
COPY ./api/routes.py /app/api/
COPY ./requirements.txt /app/
COPY ./setup.py /app/
COPY README.md /app/
COPY ./.env /app/

COPY generative_ai/__init__.py /app/genai/
COPY generative_ai/llms/llm.py /app/genai/
COPY generative_ai/llms/configs.py /app/genai/

WORKDIR /app

RUN apt-get update
RUN apt-get install gcc python3-dev -y

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -U pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -U setuptools
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -U psutil
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -e .

ENV PYTHONUNBUFFERED=1

EXPOSE 8081

CMD ["gunicorn", "--workers=2", "--timeout=3600", "--bind=0.0.0.0:8081", "api.app:create_app()"]
