FROM gcr.io/google.com/cloudsdktool/cloud-sdk
MAINTAINER Husain Al-Mohssen (husain@domain)

WORKDIR /workdir


COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

RUN mkdir /workdir/md-to-blog

COPY . /workdir/md-to-blog

WORKDIR /workdir/md-to-blog
CMD ["./run.sh"]
