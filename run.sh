#!/bin/bash

# docker entry point to build blog and copy over:

set -e 


python3 build_blog.py 
echo finished building out
echo here is outs content: 
find /md-to-blog


gsutil -m rsync -r -d -c out gs://husain.io/ 
echo synced with gs bucket

echo START DEBUG
find /md-to-blog 
echo END DEBUG

echo syncing of out folder worked
