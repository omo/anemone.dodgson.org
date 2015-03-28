+++
Tags = []
date = "2015-03-27"
title = "Travis からのアップロード"
+++

Static site generators は Travis でアップロードするのが楽らしいので真似してみる。
Travis は AWS で動いているため GitHub (これもいろいろ AWS にある)のダウンロードが速い。
Hugo の速さと相まってあっという間・・・とおもいきや
S3 に push するツール [awscli](http://aws.amazon.com/cli/) のインストールがボトルネック。
Travis いわく所用時間 11 秒. 体感は 30 秒くらい。
Go で書かれた awscli 相当のツールがあるといいのだけれど。

GitHub の Web から更新できるのは良い。これがしたかった。もうちょっと使いやすいエディタがほしい。
[Dillinger](http://dillinger.io/) はいまいち。当面は Evernote で下書きしたのをコピペしよう。
