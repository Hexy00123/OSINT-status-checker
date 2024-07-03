FROM python:3.10.14-slim

RUN apt-get update \
  && apt-get install -y curl \
  && curl -sSL https://install.python-poetry.org | python -

WORKDIR /tg_scrapper
COPY ./poetry.lock ./pyproject.toml ./
RUN /root/.local/bin/poetry install --no-root

COPY ./ ./

CMD ["/root/.local/bin/poetry", "run", "python", "-m", "src"]
