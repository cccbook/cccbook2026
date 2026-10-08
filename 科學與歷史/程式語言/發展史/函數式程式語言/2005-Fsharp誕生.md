# 2005：F# 誕生

## 事件
F# 由微軟研究院（Microsoft Research，Cambridge）的 Don Syme 設計，2005 年發表首版，2010 年隨 Visual Studio 2010 正式納入 .NET 平台成為一級語言。F# 以 OCaml 為藍本移植到 .NET：保留了 ML 家族的型別推論、代數資料型別與模式匹配，同時完全相容 .NET 的物件系統與函式庫。Don Syme 先前在 .NET 泛型（Generics，2005 年随 .NET 2.0 落地）的設計中扮演關鍵角色——F# 正是建立在「有泛型的 CLR」之上。

## 語法/特性加入的理論與實用原因

### 1. ML 核心移植到 .NET
- **理論原因**：Hindley–Milner 型別推論、代數資料型別、模式匹配是經過數十年驗證的理論基礎，理論上可與物件導向型別系統共存。
- **實用原因**：以 OCaml 為藍本可沿用成熟的語意設計；.NET 生態（GUI、資料庫、Web）直接可用，降低採用門檻。
- **彌補缺陷**：OCaml 不能使用 .NET 生態；C# 缺少函數式表達力——F# 兩邊都補上。

JVM/CLR 互操作的 F# 版：型別推論 + .NET 物件系統共存於同一份程式：

```fsharp
// 直接使用 .NET 類別庫，無需橋接層
let dict = System.Collections.Generic.Dictionary<string, int>()
dict.Add("one", 1)
printfn "%d" dict.["one"]

// ML 風格串列處理與 .NET 物件混用
open System
let today = DateTime.Today
let weekdays =
    [1..7]
    |> List.map (fun d -> today.AddDays(float d))
    |> List.filter (fun d -> d.DayOfWeek <> DayOfWeek.Saturday
                          && d.DayOfWeek <> DayOfWeek.Sunday)
```

```fsharp
// 代數資料型別與模式匹配
type Shape =
    | Circle of float
    | Rect of float * float

let area shape =
    match shape with
    | Circle r -> System.Math.PI * r * r
    | Rect (w, h) -> w * h
```

### 2. 列舉式（discriminated unions）與模式匹配
- **理論原因**：discriminated union 是 ML 的代數資料型別：封閉的「或」型別，配對模式匹配在理論上保證分解的完整性（exhaustiveness）可靜態檢查。
- **實用原因**：編譯器在新增分支時會警告漏處理的情況，重構極安全；這成為 F# 處理領域模型的主流風格。
- **彌補缺陷**：C# 當時只能用類別階層 + instanceof 模擬，冗長且無完整性檢查（C# 直到 2017 年後才補上模式匹配）。

對照組——C# 模擬代數資料型別的冗長寫法：

```csharp
// C# 2005：類別階層 + 型別檢查模擬 union，漏分支編譯器不警告
abstract class Shape { }
class Circle : Shape { public double R; }
class Rect : Shape { public double W, H; }

double Area(Shape s) {
    if (s is Circle) return Math.PI * ((Circle)s).R * ((Circle)s).R;
    if (s is Rect)   { var r = (Rect)s; return r.W * r.H; }
    throw new ArgumentException();   // 執行期才會發現漏分支
}
```

F# 的 discriminated union 一個 `type` 就表達完整的「或」型別，模式匹配還能巢狀解構：

```fsharp
// 巢狀模式匹配：直接解構運算式樹
type Expr =
    | Num of int
    | Add of Expr * Expr
    | Neg of Expr

let rec eval e =
    match e with
    | Num n -> n
    | Neg a -> -eval a
    | Add (Num a, Num b) -> a + b      // 特殊分支：兩個常數相加
    | Add (a, b) -> eval a + eval b

eval (Add (Num 1, Neg (Num 2)))   // -1
```

### 3. 非同步工作流程（async workflows）
- **理論原因**：以計算表示式（computation expression，即單子）包裝非同步邏輯：`async { ... }` 區塊內可以用看似同步的語法寫非同步程式，理論基礎是單子式組合。
- **實用原因**：2007 年 F# 1.9 就提供了 async workflows，早於任何主流語言的 async/await；I/O 並行（如爬蟲、伺服）不需回呼地獄。
- **彌補缺陷**：C# 當時的非同步程式設計只能用事件與回呼，極易出錯；F# 的 async 直接示範了更好的寫法。

對照組——C# 2005 的 Begin/End 非同步模式，回呼層層嵌套：

```csharp
// C# 2005：Begin/End 模式，錯誤處理散落各回呼，巢狀越深越難維護
WebRequest req = WebRequest.Create(url);
req.BeginGetResponse(ar => {
    var resp = req.EndGetResponse(ar);
    resp.GetResponseStream().BeginRead(buf, 0, buf.Length, ar2 => {
        int n = resp.GetResponseStream().EndRead(ar2);
        Parse(buf, n);          // 又一層回呼……
    }, null);
}, null);
```

F# 的 async 工作流程：用 `let!` 把非同步步驟串成看似同步的直線程式碼，錯誤處理回歸正常的 try/with：

```fsharp
let fetch url =
    async {
        let req = WebRequest.Create(url)
        use! resp = req.AsyncGetResponse()      // let!：等待非同步結果
        use stream = resp.GetResponseStream()
        let! body = stream.AsyncReadToEnd()
        return parse body                        // 錯誤可用 try/with 正常包覆
    }

// 三個網址並行抓取，一行組合
let all = ["https://a.com"; "https://b.com"; "https://c.com"]
         |> List.map fetch
         |> Async.Parallel
         |> Async.RunSynchronously
```

```fsharp
let urls = ["https://a.com"; "https://b.com"]
let fetchAll =
    urls
    |> List.map (fun u -> async { let! c = download u
                                  return parse c })
    |> Async.Parallel
```

### 4. 型別提供者（type providers）
- **理論原因**：2012 年 F# 3.0 推出型別提供者：在編譯期由外部資料來源（schema、資料庫、Web API）即時「生成」型別，理論上是把型別推論與外部詮釋資料結合的擦除式（erased）機制。
- **實用原因**：讀取 JSON、CSV、資料庫欄位時，IDE 直接提供強型別智慧提示，架構變更即時反映，不需手寫對應層。
- **彌補缺陷**：靜態語言處理動態資料（JSON、資料庫）時的樣板程式碼負擔。

型別提供者的呼叫樣式：宣告一個由 CSV schema 生成的強型別，欄位直接以屬性存取，不需手寫對應層：

```fsharp
// F# 3.0：CSV 型別提供者——編譯期由 Sample.csv 的 schema 生成型別
type Csv = FSharp.Data.CsvProvider<"Sample.csv">

let rows = Csv.Load("data.csv").Rows
for row in rows do
    printfn "%s：%d" row.Name row.Age    // Name、Age 是強型別屬性，
                                          // schema 變更時編譯期即報錯
```

沒有型別提供者時（如 C# 2005），同樣的工作得手寫解析與對應：

```csharp
// C#：手寫解析 + 手寫對應類別，schema 變更只能靠執行期測試發現
class Person { public string Name; public int Age; }
foreach (var line in File.ReadLines("data.csv")) {
    var parts = line.Split(',');
    var p = new Person { Name = parts[0], Age = int.Parse(parts[1]) };
}
```

### 5. 單位 of measure
- **理論原因**：在型別層次為數值附上單位（公尺、秒），理論上以擦除式的型別參數實作，不影響執行期效能。
- **實用原因**：單位錯誤（如 1999 年 NASA 火星氣候探測者號的公尺/英尺混淆）可在編譯期被攔截；QUANT 套件文化（金融與科學計算社群）使 F# 在量化金融領域特別受歡迎。
- **彌補缺陷**：所有主流語言的數值型別都不攜帶單位，單位錯誤只能靠測試或人眼檢查。

管線運算子 `|>` 是 F# 的招牌語法：資料流向與閱讀順序一致，串接出函數式管道：

```fsharp
// |> 串接：資料從左到右流過每個轉換步驟
let result =
    [1..10]
    |> List.filter (fun x -> x % 2 = 0)
    |> List.map (fun x -> x * x)
    |> List.sum          // 220

// 對照巢狀呼叫（閱讀順序與執行順序相反，可讀性差）：
let nested = List.sum (List.map (fun x -> x * x) (List.filter (fun x -> x % 2 = 0) [1..10]))
```

```fsharp
[<Measure>] type m
[<Measure>] type s
let speed = 9.8<m/s>
```

單位的實戰：單位錯誤在編譯期被攔截，NASA 火星探測者號的公尺/英尺混淆在 F# 中根本無法編譯：

```fsharp
[<Measure>] type m
[<Measure>] type ft
[<Measure>] type s

let gravity = 9.8<m/s^2>
let altitude = 100.0<m>

// altitude + 328.0<ft>          // 編譯錯誤：m 與 ft 單位不符
let altFt = altitude / 3.28084<m/ft>   // 明確轉換才能跨單位

// 距離 / 時間 推論出速度單位，全部在編譯期檢查
let time = 10.0<s>
let velocity = altitude / time        // float<m/s>，單位自動推論
```

## 彌補了什麼缺陷
F# 彌補了「C# 缺少函數式表達力、OCaml 不能用 .NET 生態」的雙向缺陷。它與 C# 產生了著名的互相影響：F# 的 async workflows（2007）直接啟發了 C# 的 async/await（2012，同樣由 Don Syme 周邊的微軟團隊設計），F# 的模式匹配也促成 C# 2017 年後的模式匹配擴展。F# 成為 .NET 平台上函數式程式設計的旗艦語言。

## 相關條目
- [1996-OCaml誕生](1996-OCaml誕生.md)
- [2004-Scala誕生](2004-Scala誕生.md)
- [2010-Haskell2010標準](2010-Haskell2010標準.md)
