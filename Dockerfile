FROM python:3.9.6-alpine3.14

# set work directory

WORKDIR /myApp

RUN mkdir /myApp/staticfiles
RUN mkdir /myApp/media

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib zlib-dev

# install dependencies
RUN pip install --upgrade pip
ADD requirements.txt .

RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /myApp/entrypoint.sh
RUN chmod +x /myApp/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/myApp/entrypoint.sh"]
