#!/bin/bash

# docker entry point to build blog and copy over:

python3 build_blog.py && gsutil -m rsync -r -d -c out gs://husain.io/ || echo "👹gsutils failed👹"
