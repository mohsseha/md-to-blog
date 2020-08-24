FROM gcr.io/google.com/cloudsdktool/cloud-sdk
MAINTAINER Husain Al-Mohssen (husain@domain)

WORKDIR /


COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

RUN mkdir md-to-blog

COPY . md-to-blog 

WORKDIR /md-to-blog
CMD ["./run.sh"]
