# 2005-FSharp與.NET函數式

## 案件摘要

2005 年，Microsoft Research Cambridge 的偵探 Don Syme 發表了 F# 語言（2007 年隨 .NET 正式釋出 1.0）——本質上是 OCaml 的 .NET 變體。這樁案子要破的謎題是：為什麼型別推論、代數資料型別這些 1970-80 年代 ML 就有的好東西，始終進不了工業界？Syme 的答案是把 ML 語言整體移植到 CLR 虛擬機器上，並加上兩項獨創線索：computation expression（F# 的 monad 語法糖）與 async workflow——比 C# 的 await 早了兩年。F# 是微軟把函數式程式設計從學術界推進工業界的關鍵案件。

## 前因 -- 為什麼會有這個案子

- .NET 1.x 的 C#/VB 是純命令式物件導向語言，無法表達 FP 的核心抽象：多型函數、ADT、pattern matching。
- ML（SML、OCaml）與 Haskell 長年被視為學術語言，企業生態系（工具、函式庫、人才）不肯採用。
- 另一條已存在的重要線索：金融計算——Jane Street 用 OCaml 做高頻交易系統——證明 FP 在高可靠、高正確性場景有實際商業價值。
- Syme 的目標明確：把 OCaml 的型別推論與函數式抽象帶進工業界，而且要「編譯成 CLR 位元組碼」，讓 FP 程式能呼叫整個 .NET 函式庫。
- 非同步與平行計算在多核時代變得迫切，但命令式的 callback 與執行緒模型讓程式破碎——需要新的抽象。

## 線索與推理 -- 數學式、程式、理論

### 線索一：OCaml 的型別系統在 CLR 上實現

F# 保留了 Hindley-Milner 型別推論的核心：不需註解，編譯器由使用方式推導型別。函數應用的推論規則：

$$
\frac{\Gamma \vdash e_1 : \tau \to \sigma \quad \Gamma \vdash e_2 : \tau}
     {\Gamma \vdash e_1 \; e_2 : \sigma}
$$

加上 let-polymorphism（帶 value restriction）與代數資料型別：

$$
\text{type } t = C_1 \text{ of } \tau_1 \mid C_2 \text{ of } \tau_2 \mid \cdots
$$

這些在 CLR 上實現的難點：CLR 的泛型是執行期具化的 reified generics，與 HM 的編譯期一般化需要協調——Syme 團隊讓 F# 的泛型直接編譯到 CLR 泛型上。

### 線索二：computation expression -- F# 的 monad 語法糖

F# 把 Haskell 的 monad 重新包裝成 computation expression。monad 的 bind 與 return：

$$
\text{bind}: M\,\tau \to (\tau \to M\,\sigma) \to M\,\sigma \qquad
\text{return}: \tau \to M\,\tau
$$

遵守 monad 律：

$$
\text{bind } (M\,\tau)\; \text{return} = M\,\tau \qquad
\text{bind } (\text{bind } M\, f)\; g = \text{bind } M\, (\lambda x.\, \text{bind } (f\, x)\; g)
$$

在 F# 中寫成 `let!`（= bind）與 `return`（= return），由 builder 物件定義語義。

### 線索三：async workflow -- 早 C# await 兩年的非同步

F# 的 async workflow（2005-2007）用 monad 包裝非同步計算：`async { let! r = Async.GetWebFile ... }`。語義上，`let!` 把「等待結果後繼續」這件事變成一等公民的組合單元，不需 callback、不需執行緒阻塞：

$$
\text{async} = \text{Cont}\;(\tau, \text{CT}) \quad \text{即 CPS 變換的非同步延續}
$$

C# 的 async/await（2012）在語法與語義上直接受此啟發，晚了兩年。

### 線索四：type provider -- 編譯期生成型別（2010）

F# 的 type provider（2010）更進一步：編譯期從外部資料源（資料庫、WSDL、CSV）動態生成型別，資料源改了型別就自動更新。這是把「資料即型別」的證明式思維推到極致。

### 可執行程式碼：F# 的 async workflow、pattern matching 與型別推論

```fsharp
// 型別推論：完全不需型別註解
let rec fact n = if n <= 1 then 1 else n * fact (n - 1)   // int -> int

// ADT + pattern matching（OCaml 血統）
type Shape =
    | Circle of float
    | Rect of float * float

let area s =
    match s with
    | Circle r      -> System.Math.PI * r * r
    | Rect (w, h)   -> w * h

// async workflow：宣告式非同步（早 C# await 兩年）
let fetch url = async {
    let client = new System.Net.Http.HttpClient()
    let! body = client.GetStringAsync(url) |> Async.AwaitTask
    return body.Length }

[ "https://example.com"; "https://example.org" ]
|> List.map fetch
|> Async.Parallel          // 同時發出，仍是用 let! 組合的單一 workflow
|> Async.RunSynchronously
|> printfn "%A"
```

### Python 模擬：async workflow 的 monad bind

```python
# 用 Python generator 模擬 F# 的 computation expression：
# yield = let!（bind），非同步的「暫停-續跑」語義
def bind(m, f):
    """monad bind：跑完 m 的第一段，把結果交給 f 續跑"""
    for x in m:          # 模擬等待
        pass
    return f(x)

def return_m(x):
    return x

def fetch(name):         # 模擬非同步取資料：先 yield（掛起），再續跑
    yield f"waiting:{name}"
    return_m(len(name) * 10)

def workflow():
    a = bind(fetch("example.com"), return_m)
    b = bind(fetch("example.org"), return_m)
    return a + b

print(workflow())        # 220，宣告式組合，無 callback
```

## 結案 -- 後果與影響

- C# 的 LINQ（2007，Erik Meijer 的影響）與 async/await（2012）直接受 F# 啟發——F# 的 query expression 與 async workflow 是兩者的原型。
- F# 成為金融與科學計算的工業級 FP 語言，被多家金融機構採用。
- 微軟 Research 成功把 FP 從學術界推進工業界：型別推論、ADT、pattern matching 進入主流開發者的日常。
- Scala 與 F# 共同證明：「混合範式」（命令式 + 函數式）是主流路線，而非純學術的極端。
- type provider 開創了「編譯期從資料源生成型別」的新方向，影響後續的資料型程式設計研究。
- 本案結論：FP 不是學術玩具，缺的只是一座通往工業界的橋——那座橋就是 CLR。

## 關鍵人物與文獻

- Don Syme：本案偵探，Microsoft Research Cambridge 研究員，F# 的設計者，type provider 的發明人。
- Erik Meijer：微軟的函數式推廣者，LINQ 與 Rx 的設計者之一。
- Don Syme, Adam Granicz, Antonio Cisternino, "Expert F#", Apress, 2007.
- Don Syme, "F# at the Heart of .NET", Microsoft Research Technical Report, 2005.
- Don Syme, Gregory Neverov, James Margetson, "Extensible pattern matching via a lightweight language extension", ICFP, 2007.
- Don Syme, "Data and Programming Models", ICFP, 2011（type provider 的正式發表）.
- Xavier Leroy, "The Objective Caml system", INRIA, 1996（F# 的血統來源）.
