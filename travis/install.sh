#!/bin/sh
pip install awscli
mkdir -p out
curl -L https://github.com/spf13/hugo/releases/download/v0.18.1/hugo_0.18.1_Linux-64bit.tar.gz > out/hugo.tgz
cd out && tar xvf hugo.tgz
