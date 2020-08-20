FROM python:3.8
MAINTAINER Husain Al-Mohssen (husain@domain)

WORKDIR /root

RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

RUN mkdir md-to-blog

COPY . md-to-blog 
COPY .git md-to-blog/

WORKDIR /root/md-to-blog
CMD ["python3" , "build_blog.py"]
