#!/bin/sh

mkdir -p out
curl -L https://github.com/spf13/hugo/releases/download/v0.13/hugo_0.13_linux_amd64.tar.gz > out/hugo.tgz
cd out && tar xvf hugo.tgz
