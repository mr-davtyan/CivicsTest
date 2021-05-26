# Dockerfile

FROM python:3.8.3-alpine

ENV CIVICS_TEST=/opt/CivicsTest
#RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory

RUN mkdir -p $CIVICS_TEST

# where the code lives
WORKDIR $CIVICS_TEST

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk del build-deps \
    && apk --no-cache add musl-dev linux-headers g++
# install dependencies
RUN pip install --upgrade pip
# copy project
COPY . $CIVICS_TEST
RUN pip install -r requirements.txt

CMD ["/bin/bash", "/opt/CivicsTest/start-server.sh"]