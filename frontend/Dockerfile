FROM python:3.10.14-slim

EXPOSE 8501

WORKDIR /frontend
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["streamlit", "run", "src/Main.py"]