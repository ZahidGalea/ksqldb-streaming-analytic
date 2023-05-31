FROM python:3.9.9
WORKDIR app

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry lock
RUN poetry install

COPY visualization.py .
COPY ksql_rest.py .
# ENTRYPOINT ["python","-u","main.py"]