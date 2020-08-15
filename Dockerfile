FROM python:3.8
MAINTAINER Husain Al-Mohssen (husain@domain)

WORKDIR /root

RUN curl -sSL https://sdk.cloud.google.com | bash

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

RUN mkdir in
RUN mkdir theme

COPY *.py . 

COPY in ./in 
COPY theme ./theme

CMD ["python3" "build_blog.py"]
