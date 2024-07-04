FROM python:3.10.14-slim

WORKDIR /frontend
COPY ./ ./

EXPOSE 8501
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "src/Main.py"]
