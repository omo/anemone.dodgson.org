+++
Tags = []
date = "2015-04-08"
title = "Web Push Protocol"
draft = false
+++

"[Generic Event Delivery Using HTTP Push](https://tools.ietf.org/html/draft-thomson-webpush-http2-02)" なる RFC を知った。
JavaScript の [Push API](https://w3c.github.io/push-api/) をネットワークレベルでどう実現するか決めるものらしい。
Push API, システムが提供する [GCM](https://developer.android.com/google/gcm/index.html) なんかのラッパーだと思い込んでいた。
Chrome の現状はそのようだけど、標準的にはスタック全体を定義しようとしている模様。
仕様を書いているのは Mozilla の人。えらい。

Web Push は HTTP/2 の上に定義されており、`PUSH_PROMISE` で UA にメッセージを送る。
TCP で現実的なプッシュを作れるとは思っていなかったので驚いた。
ざっと調べてみたところ GCM も TCP ベースらしい。
接続を保つべく適当な間隔で heartbeat していると、世間の資料にはある。
SMS など cell network の技術は使わないのか。
もっとも Wi-Fi だけでも動かす手前 TCP 頼みは仕方がない? よくわからないな。
Web Push の仕様は SMS を使うなど適当な方法でそれらモニタリングを置き換えて良いと断っている。

`PUSH_PROMISE` 以外で面白いところ: 個々のメッセージは URL を持たない。
URL は Subscription 単位(=UA 単位)で割り振られる。メッセージの到達も保証しない。
適当に expire するのでアプリケーションはメッセージがドロップされてもちゃんと動くように書けと注意している。
トランザクションとか言い出さないあたり、地に足が付いている。好感。
Heartbeat の方法も指示しない。HTTP/2 の `PING` を使えということだろう。下にあるプロトコルの出来が良いとラクだ。

Web Push をブラウザの外、たとえばサーバ間、あるいはデスクトップアプリで使うのはどうか。
XMPP でいい気もすれど、セマンティクスの違いや単純さから Web Push を選ぶのもそれはそれで悪くないかも。
ACK がないとだめかな。
あとは GCM の代替実装としてフルスタックを揃えると
Cyanogen などの Forked Android 勢に喜ばれるかもしれない。HTTP/2 実装の普及が待たれる。
