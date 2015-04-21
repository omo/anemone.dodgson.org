+++
Tags = []
date = "2015-04-22"
title = "Rust の Lifetimes"
draft = true
+++

[もうすぐ 1.0](http://blog.rust-lang.org/2015/02/13/Final-1.0-timeline.html) という Rust。
久しぶりに[チュートリアル](http://doc.rust-lang.org/nightly/book/)を読む。以前見た時は不可解な機能が多く、こりゃ難しさに溺れて死にそうだな・・・と思っていた。今見るとずいぶんすっきりしている。単純さに舵を切れたのはえらい。

チュートリアルに登場したうちわからなかった機能は 2 つ, Lifetimes と Macros。Macros はさておき Lifetimes は理解してよさそう。詳しい情報を求めて[リファレンス](http://doc.rust-lang.org/nightly/reference.html
)をひやかす。驚くほど何も書いてない。かわりに元ネタとしてメモリ安全な C の方言 [Cyclone](http://cyclone.thelanguage.org/) による region based memory management が言及されている。勢いでその資料にも目を通す。[解説PDF](http://www.cs.umd.edu/projects/cyclone/papers/cyclone-regions.pdf)ひとつと[マニュアルの一部](http://cyclone.thelanguage.org/wiki/Memory%20Management%20Via%20Regions/)。どちらもよく書けていた。記法も Rust の lifetimes と似ている。

Cyclone の region based memory management では、フレームに確保したメモリの出処、つまりメモリの生存期間を、そのメモリを指すポインタ変数に型の一部としてくっつける。この生存期間が Regions. 型は総称的で、その総称性を通じ関数の呼び出し元から呼び出し先へと変数毎の reigons が伝わっていく。そして長い regions のポインタに 短い regions のポインタを代入しようとすると型チェックでエラーになる。だから dangling pointer がおきない。

全てのポインタ変数が型に regions を持っている。関数の引数も同じ。そう聞くと仰々しいけれど、大抵はデフォルトの型でうまく動く。そしてデフォルトを使うかぎりコード上に regions は姿を見せない。だから普段は気にしなくて良い。Cyclone だと C からの移植で 8 割くらいは元のコードそのままでよかったという。それでも時々 lifetimes を指示したい場面があり、region 記法の出番となる。

Rust の仕組みはだいたい Cyclone と同じに見える。生存区間を表す型を Cyclone では Regions, Rust では Lifetimes と呼ぶ。Rust の reference すなわちポインタは, 変数の型に (多くは暗黙の) regions を含んでいる。

Lifetimes はコールスタックというかフレーム上のメモリの寿命をトラックするための仕組み。だから lifetimes の寿命は呼び出し関係に応じた入れ子になっている。ヒープに確保したオブジェクトの動的な寿命をトラックして正当性を担保するのは lifetimes の仕事ではない。ヒープへの reference も取りだすことはできるけれど、その reference の lifetime はヒープを指す変数があるフレームのスコープに紐づく。ヒープ上のメモリが関数のスコープを超えて outlive する事実を lifetimes で表現することはできない。

ではヒープにあるメモリの寿命はどう守るかというと、`Box` (`unique_ptr` 相当), `RC`, `Arc` (`shared_ptr` 相当) といったスマートポインタぽい型, move semantics と RAII がうまくやってくれる。ヒープへの reference を取り出すことはできる。ヒープとフレームの交わるところ、ヒープを指す reference の妥当性は、ownership の borrowing 機構と borrowing が強制する imutability によって保証される。RAII-Move-Borrowing-Lifetimes の組み合わせが memory safety を実現する。この結論にたどり着いたのはえらい。デザインの勝利だと思う。たとえば Cyclone には汎用的な RAII が無いなどヒープの管理には大した工夫がなく、普通に Boehn GC を使っていると書いてあった。Rust のような GC-less にはできてない。

安全なぶん厳しい制限でもある。C++ と同じようにコードを書くわけにはいかなそう。いままで曖昧に済ませていた細部をよく考えないといけない。自分が混乱したのも lifetimes とヒープの関係が曖昧だったせい。おもったより寿命にルーズだった自分に気付く。

Rust には安全でないメモリを扱う raw pointer もある。どのくらいの頻度で raw pointer が必要になるのだろうか。動的サイズの配列 Vec 型の実装では raw pointer が使われていた。C++ で replacement new を呼んだり destrucdtor を明示的に呼んだりする程度に必要なかんじかしら。つまりしょぼいコードを書いてる分には必要ない。めでたい。
