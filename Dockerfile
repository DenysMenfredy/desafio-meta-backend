FROM python:3.9

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /src

COPY poetry.lock pyproject.toml /src/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /src/

EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

