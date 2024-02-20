FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

RUN pip3 install pytest==8.0.0
RUN pip3 install requests
RUN pip3 install xmltodict

COPY iss_tracker.py /code/iss_tracker.py
COPY test_iss_tracker.py /code/test_iss_tracker.py

RUN chmod +rx /code/iss_tracker.py
RUN chmod +rx /code/test_iss_tracker.py

ENV PATH="/code:$PATH"