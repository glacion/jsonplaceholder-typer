FROM python:3.6-slim AS resolver
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry export -f requirements.txt -o requirements.txt

FROM python:3.6-slim
WORKDIR /app
COPY --from=resolver /app/requirements.txt .
COPY jsonplaceholder ./jsonplaceholder
COPY tests ./tests
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT [ "python", "./jsonplaceholder/main.py" ]