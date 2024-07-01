FROM 3.11.9-bookworm

WORKDIR /tg_scrapper

COPY ./tg_scrapper/requirements.txt /tg_scrapper/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tg_scrapper/requirements.txt

COPY ./tg_scrapper /tg_scrapper
WORKDIR /tg_scrapper

CMD ["python3", "-m", "src"]
