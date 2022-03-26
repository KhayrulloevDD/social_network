FROM python:3
ENV PYTHONUNBUFFERD 1
WORKDIR /social_network
COPY requirements.txt /social_network/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
