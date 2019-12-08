#!/bin/sh
pip install awscli
mkdir -p out
curl -L https://github.com/gohugoio/hugo/releases/download/v0.60.1/hugo_0.60.1_Linux-64bit.tar.gz > out/hugo.tgz
cd out && tar xvf hugo.tgz
