+++
Tags = []
date = "2015-03- 27"
title = "Travis からのアップロード"
+++

Static site generators は Travis でアップロードするのが楽らしいので真似してみる。
Travis は AWS で動いているため GitHub (これもいろいろ AWS にある)のダウンロードが速い。
Hugo の速さと相まってあっという間・・・とおもいきや
S3 に push するツール [awscli](http://aws.amazon.com/cli/) のインストールがボトルネック。
Travis いわく所用時間 11 秒. 体感は 30 秒くらい。
Go で書かれた awscli 相当のツールがあるといいのだけれど。
