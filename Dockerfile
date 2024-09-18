FROM python:3.11

WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONUNDONTWRITEBYTECODE 1

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "todoproject.wsgi:application", "--bind", "0.0.0.0:8000" ]