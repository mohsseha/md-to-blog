FROM python:3.8
MAINTAINER Husain Al-Mohssen (husain@domain)

WORKDIR /root


COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY *.py . 


CMD ["python3"]
