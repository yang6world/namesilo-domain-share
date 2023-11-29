FROM python:3.11-alpine
LABEL authors="Y"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]