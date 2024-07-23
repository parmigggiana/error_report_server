FROM python:3.12-alpine

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py
COPY templates templates

EXPOSE 9999
CMD [ "uvicorn", "main:app", "--port", "9999" ]