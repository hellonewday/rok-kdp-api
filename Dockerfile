# FROM python:3.8
# WORKDIR /app
# COPY . /app

# RUN pip install -r requirements.txt
# EXPOSE 5000
# ENTRYPOINT ["python"]
# CMD ["app.py"]

FROM python:3.8-slim

WORKDIR /app

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]