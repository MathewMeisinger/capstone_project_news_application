# python image
FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# set work directory
WORKDIR /code


# install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/

# expose Django port
EXPOSE 8000

# run djangos development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]