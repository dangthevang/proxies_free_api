FROM python:3.8

MAINTAINER vangdt

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install django

COPY ./requirements.txt /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 3030

CMD ["python", "manage.py", "runserver"]







