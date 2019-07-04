FROM python:3

COPY . /

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "server.py"]