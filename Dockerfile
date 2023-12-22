FROM python:3.9.15-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 27017
ENTRYPOINT ["python3", "-m", "gunicorn", "-b", ":8080", "api:app"]