FROM debian:buster-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM gcr.io/distroless/python3-debian10
COPY --from=build-venv /venv /venv
COPY . /app
WORKDIR /app
RUN ENV=CI /venv/bin/python3 -m pytest
ENTRYPOINT ["/venv/bin/python3", "-m", "gunicorn", "-b", ":8080", "api:app"]