FROM python:3.8.5

WORKDIR /crud_users

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD python manage.py migrate --no-input

CMD python manage.py runserver
