+++
Tags = []
date = "2015-04-28"
title = "Custom Views の気楽さ加減"
draft = false
+++

唐突に Android 入門日記。

余暇につくっている小さな Android アプリを [Hierarchy Viewer](http://developer.android.com/tools/help/hierarchy-viewer.html) で眺めてみた。性能上 View tree はフラットなほど良い。自分のアプリは思ったよりツリーが深くてげんなり。

Custom Elements や React Componentsと同じノリで沢山の Custom View を定義しているのがまずいのだろうか。状態を持たせるためだけに `View` のサブクラスをつくっている。各 custom view はコンストラクタで `inflate()` してサブツリーを作り、それを表示する。`View#onDraw()` は override しない。今のところ必要がない。

このやり方で custom view のレイアウトを与えると、ルートとなる View (大抵はなんらかの Layout クラス) が自分自身とは別に必要。ルートになれる View は一つだけ。この制限がなければ custom view 自身がその Layout クラスを継承すれば済むのに、XML の構文だけが理由で単一ルートというこの制限を受ける。Custom view -> LinearLayout -> 本来の sub view ... と一段 View 階層が深くなってしまう。やや理不尽。

## Activity, Fragment

人々はどうしているのだろう。サンプルアプリの親玉 [iosched](https://github.com/google/iosched) を覗く。アプリの規模と比べて custom view の数は少ない。20 個くらい。むしろ Activity や Fragment の方が多そう。

Custom view を使わないなら、どのように View をグループ化するのか。

ある程度の規模があるまとまりには Fragments を使っている。Responsive にしない画面では Activity にベタな layout を流し込んで終わり。自分が custom view を作りたくなる典型的なケース、`RecyclerView` の個々のアイテムにも custom view は作らない。適当な layout を inflate し、そのサブツリーに必要な状態やイベントリスナをくっつけておわり。たしかにこれなら余計な階層はできない。でもオブジェクト指向の敗北みたいでなんとなく悲しい。Adapter の `getView()` が巨大になるし・・・

## ViewHolder

オープンソースの Twitter クライアント [Talon](https://github.com/klinker24/Talon-for-Twitter
) を覗く。すると状態は ViewHolder という呼ばれるクラスを定義し `View#setTag()` で個々の View に紐付けている。たしかにこれなら View を継承しなくて済みそう。よく見るとオフィシャル文書でも[紹介されている](http://developer.android.com/training/improving-layouts/smooth-scrolling.html)パターン。主に性能上の理由で使えと言ってるけど、ここに振る舞いや状態を与えてもよさそうじゃない？ダメ？

ViewHolder はパターンにすぎず、必ずしも決まった型があるわけではない。ただ `RecyclerView` には `RecyclerView.ViewHolder` なんてクラスもある。これを使うのが流儀なのかね。

さて custom view を定義するのはいつなのか。
再利用可能な部品を作る時、特殊な描画が必要なときに使っているように見える。

少ないサンプルから得た自分の理解をまとめると:

 * レイアウトを inflate してリスナや値を差し込めば済むケースではいちいち Custom View を作らない。
 * 粒度の大きな View の集まりは Fragment でグループ化する。主に responsive な画面をつくるため。
 * Fragment が必要ないなら Activity だけで済ますのもあり。
 * リストの要素など小さなまとまりには ViewHolder クラスを定義して状態をまとめ、そのインスタンスをサブツリーのルートに `setTag()` する。
 * 凝った描画をしたいときや再利用可能な汎用 View 部品は custom view にする。

今書いているコードと結構違ってしまうなあ・・・。

## アンチ Fragment の Custom View

ふと思い立ち Jake Wharton のサンプルアプリ [u2020](https://github.com/JakeWharton/u2020) を覗いてみる。この人はカジュアルに custom view を定義している。ただしそうした View 自身は subview を inflate しない。Adapter が custom view をルートとする layout を inflate する。これなら余分な view のネストは発生せず、かつ custom view を view tree のカプセル化に使う馴染み深いスタイルを踏襲できる。先の iosched なら Fragment を使いそうな場面でこうなっているのは、彼らが[アンチ Fragment 派](https://corner.squareup.com/2014/10/advocating-against-android-fragments.html)だからかもしれない。

Adapter に inflate させると本来は View が隠すべき詳細たるレイアウトが漏れ出ている気がするけれど、一方で `onFinishInflate()` など View 標準のライフサイクルに則りやすくなるのはよい。このバランスがちょうどいいかも。

この流儀では:

 * View ツリーをまとえる手段としても気軽に Custom View を定義して良い。
 * Custom View のインスタンス化は全体を Inflater に任せ、View を直接 new したり View 自身に inflate() させたりしない。

## 大げさ加減

Custom view は大げさで、わざわざそれが欲しくなるほどの複雑さは多くないとも聞いた。抽象の厚さには好みもあるので一概には言えないけれど、たしかに inflate して OnClickListener つけておわりくらいなら custom view はいらなそう。どうせクラスがないなら functional な感じにかけるとかっこいいんだけどなー・・・

 * まとまりをつくるのに新しいクラスが必要とは限らない

----
 
 ドラフトにコメントをくれた [@karino2012](https://twitter.com/karino2012/with_replies) ありがとう。
