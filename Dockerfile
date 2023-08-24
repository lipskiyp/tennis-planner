# Base imgae
FROM python:3.11.4-alpine3.18
LABEL maintainer = "https://github.com/lipskiyp"

# Ensure real-time logs
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 9000

# Create new virtual environment
RUN python -m venv /py && \
    # Update pip
    /py/bin/pip install --upgrade pip && \
    # Install postgres client
    apk add --update --no-cache postgresql-client && \
    # Install postgres dependecnies inside temporary virtual environment
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # Install dependencies
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Remove /tmp
    rm -rf /tmp && \
    # Remove temporary virtual environment
    apk del .tmp-build-deps && \
    # Add user
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

# Assign default user
USER django-user