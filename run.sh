#!/bin/bash

#curl -sSL https://sdk.cloud.google.com | bash
#export PATH=$PATH:/root/google-cloud-sdk/bin

#python3 -m pip install -r requirements.txt --no-cache-dir

python3 build_blog.py

gsutil -m rsync -r -d out gs://husain.io/
