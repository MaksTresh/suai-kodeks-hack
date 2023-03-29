FROM python:3.11.2
WORKDIR /app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt install -y zip htop screen libgl1-mesa-glx

COPY requirements.txt .
COPY requirements.ml.txt .

RUN pip install -r requirements.txt
RUN pip install -r requirements.ml.txt

COPY . .