FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN pip install pytest==8.0.0
RUN pip install requests
RUN pip install xmltodict
RUN pip install flask

COPY iss_tracker.py /app/iss_tracker.py
COPY test_iss_tracker.py /app/test_iss_tracker.py

ENTRYPOINT ["python"]
CMD ["iss_tracker.py"]
