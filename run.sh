#!/bin/bash

# docker entry point to build blog and copy over:

set -e 


#python3 build_blog.py 

find . 
gsutil -m rsync -r -d -c out gs://husain.io/ 
# test
