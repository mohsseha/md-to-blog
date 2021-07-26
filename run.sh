#!/bin/bash

set -e # stop if there is an error

gsutil cp gs://husain-io-tmp/ssh/service-account-husain.io ~/.ssh/id_rsa 
chmod 400 ~/.ssh/id_rsa
ssh-keyscan github.com >> ~/.ssh/known_hosts
git config --global user.email "service_account@husain.io"
git config --global user.name "service account GCP Builder"


echo DEBUG: 
cat ~/.ssh/known_hosts

python3 build_blog.py


cd /workdir

git clone --progress --verbose git@github.com:mohsseha/mohsseha.github.com.git

rm -fr /workdir/mohsseha.github.com/*
#copy new webpage to output repo: 
cd /workdir
cp -a md-to-blog/out/. mohsseha.github.com/

# push new webpage back to github: 
cd mohsseha.github.com/
date > last_build_time.md # used for testing
git add .
git status 
git commit -a -m "auto generated commit message from svs account. See run.sh in github.com/md-to-blog"
git push 

echo  ✅ done ✅ 
