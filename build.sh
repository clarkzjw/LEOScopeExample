#!/usr/bin/env bash

set -x
commit=`git rev-parse --short HEAD`
tag=`date -u +%Y%m%d-$commit`
branch=`git branch | grep \* | cut -d ' ' -f2`

sudo docker build -t clarkzjw/leoscope_example:$tag .
sudo docker push clarkzjw/leoscope_example:$tag

if [[ "$branch" == "master" ]]; then
  sudo docker tag clarkzjw/leoscope_example:$tag clarkzjw/leoscope_example:latest
  sudo docker push clarkzjw/leoscope_example:latest
fi
