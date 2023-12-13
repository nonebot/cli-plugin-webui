ARG SOURCE_COMMIT=
ARG PYTHON_IMAGE=3.11
ARG VARIANT=

FROM python:${PYTHON_IMAGE}${VARIANT:+-$VARIANT} AS build-stage

RUN pip install poetry

COPY . /app

WORKDIR /app

RUN poetry install \
    && poetry run nb self install .

FROM python:${PYTHON_IMAGE}${VARIANT}

EXPOSE 8080

ENV WEBUI_BUILD=${SOURCE_COMMIT} \
    HOST=0.0.0.0 \
    PORT=8080

CMD poetry run nb ui run --port $PORT --host $HOST

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD httpx --verbose --follow-redirects http://127.0.0.1:${PORT}
