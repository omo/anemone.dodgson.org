+++
Tags = []
date = "2015-06-15"
title = "FTrace と Systrace"
draft = false
+++

[Systrace](http://developer.android.com/tools/help/systrace.html) を使いたいとおもい調べた記録。

[Ftrace](https://www.kernel.org/doc/Documentation/trace/ftrace.txt) は Linux カーネルのプロファイル(トレーシング)機構。Ftrace にはざっと三つの構成要素がある:
1. Linux の debugfs を介して操作するトレース情報のバッファリング機構、
2. 2. カーネル標準で用意されているいくつかの標準probe(トレーシング情報)、
3. 3. コンパイラのプロファイリングオプションを介して全てのカーネル内関数に注入されるフック。

Ftrace の機能はコンパイル時スイッチでオフにできる。特に 3 のコンパイラ経由のフックはオフにされていることがあるっぽい。若干のオーバーヘッドがあるため。
手元の Ubuntu では有効になっていた。

Android の Systrace は ftrace のインフラを使って作られている。
Android のトレーシング機構 Systrace は 3 に頼らず必要な情報をとれるよう, Android 自身がフレームワークのコードとかに probe を入れている。

Solaris 出身で最近は Linux チューニングに熱心な性能改善エキスパート Brendan Gregg が、少し前から [ftrace スゲーサイコー](https://lwn.net/Articles/608497/)と騒いでおり何かと思っていた。彼は 3 が気に入っているのだな。Solaris のカーネルはは色々ながんばりの結果 3 相当がきっちり動き、おかげで DTrace が使える。Brendan Gregg は Linux の性能モニタリングが弱いとよく不満を書いているけれど、ftrace に DTrace 代替としての可能性を見出し喜んでいるのだろう。

Brendan Gregg がもう一つ騒いでいる Linux カーネルの要素技術に eBPF がある。BPF/eBPF は Linux カーネルに入っているミニ言語処理系で、パケットフィルタなんかを書くのに使われているという。Chrome も Linux 版のサンドボックス機構に eBPF を使っており、システムコールの引数をチェックして不正な呼び出しを殺したりしている(らしい)。自分はそれで名前だけ知っていた。

Brendan Gregg にとって eBPF は DTrace の D 言語相当なのだろう。Ftrace でカーネルのあちこちにフックを差し込めるようになり、そのフックのなかで eBPF のプログラムを動かして欲しいデータを数える。これで Linux 版 DTrace のできあがり・・・みたいなイメージと思われる。こうやって声の大きいユーザが欲しいものアピールするのは良い話な気がする。DTrace 相当までの道のりは遠そうだけどがんばってほしい。じっさい [Tracing で使う試みはある](https://lwn.net/Articles/599755/) ぽい。

もっとも Android アプリ開発者としてはそこまで立ち入るまでもなく、というか立ち入りようがない。
当分は Systrace をよく理解しておく方がよさげだな。
