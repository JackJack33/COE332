FROM python:3.9

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "src/api.py"]
CMD ["python", "src/worker.py"]
