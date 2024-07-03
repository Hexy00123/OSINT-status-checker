FROM python:3.10.14-slim

COPY ./poetry.lock ./pyproject.toml /backend/
WORKDIR /backend

RUN apt-get update \
  && apt-get install -y curl \
  && curl -sSL https://install.python-poetry.org | python - \
  && echo PATH="/root/.local/bin:$PATH" >> /root/.bashrc \
  && /root/.local/bin/poetry install --no-root

COPY ./ ./

CMD ["/root/.local/bin/poetry", "run", "python", "-m", "src"]
