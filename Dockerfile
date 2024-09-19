FROM python:3.11

WORKDIR /code

ENV PYTHONUNBUFFERED=1
ENV PYTHONUNDONTWRITEBYTECODE=1

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 todoproject.todoproject.wsgi:application