FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install flask requests

CMD ["python", "app.py"]
