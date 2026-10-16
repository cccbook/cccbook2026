# 2000 C# 與 .NET：微軟的絕地反攻

## 案發現場

2000 年 6 月 22 日，微軟在 professional developers conference 上宣布了 .NET 平台與一門新語言 C#。這不是一次平常的產品發表，而是一場被逼到牆角的反擊。

要理解這場反擊，得回到 1995 年。Sun 推出 Java，打出「Write Once, Run Anywhere」的旗號，用虛擬機（JVM）與位元組碼技術讓程式跨平台執行。更狠的是，Java 挾著網路時代的氣勢，搶走了微軟視為命根的企業伺服器市場。1997 年，Sun 甚至告上法院，指控微軟在 Windows 上的 Java 實作違反授權合約——因為微軟偷偷加了自己的專屬擴充，破壞了 Java 的可攜性。

站在微軟工程師的角度，這場訴訟案發現場遺留的是一個無解的困境：**繼續用別人的語言，就要遵守別人的規則；自創平台，就得重新說服整個世界。** 微軟需要一門「自己的 Java」——不只是語言，而是一整套執行環境、類別庫與工具鏈。

為何重要？因為這標誌著虛擬機技術從 Sun 的一枝獨秀，變成兩大陣營的正面對決。VM 時代正式拉開序幕。

## 偵查過程

微軟把這個任務交給了 Anders Hejlsberg——這位丹麥工程師堪稱語言設計史上的傳奇：他在 1980 年代寫出 Pascal 編譯器（Turbo Pascal 的靈魂），後來在 Borland 設計 Delphi。1996 年跳槽微軟後，先主導了 Visual J++，訴訟之後順理成章地接下新語言的設計。

Hejlsberg 的推理路徑清晰可循：

**第一，VM 與中間語言。** Java 的成功證明了「高階語言 → 位元組碼 → 虛擬機執行」這條路可行。微軟照樣畫了這張圖，但設計得更通用：CLR（Common Language Runtime）執行的不是「某種 Java 位元組碼」，而是 CIL（Common Intermediate Language，又稱 MSIL）。任何語言只要編譯成 CIL，就能在 CLR 上執行。

$$
\text{Source} \xrightarrow{\text{compiler}} \text{CIL} \xrightarrow{\text{JIT}} \text{native code}
$$

這個「中間語言」的思路其實源自更早的 UCSD Pascal p-code 與 Smalltalk 的位元組碼，但 CLR 把「多語言共享一個執行環境」推到了極致：不只 C#，微軟同時推出了 VB.NET、Managed C++，後來社群更讓 F#、IronPython、IronRuby 都能在 .NET 上跑。Java 世界裡 JVM 上跑的是「Java 系」語言；CLR 則從第一天就宣稱：**語言只是外殼，執行環境才是核心。**

CIL 本身是一種棧式虛擬機指令集。以兩數相加為例，CIL 長這樣：

```cil
ldc.i4 3        // 把 3 推上堆疊
ldc.i4 4        // 把 4 推上堆疊
add             // 彈出兩值相加，結果推回堆疊
call void [mscorlib]System.Console::WriteLine(int32)
```

**第二，屬性（property）與委派（delegate）。** Hejlsberg 從 Delphi 帶來了兩件 Java 沒有的武器：

- **Property**：讓欄位存取可以用語法糖包裝，呼叫端寫 `obj.Name = "x"`，實際執行的是 getter/setter 方法。這解決了「直接暴露欄位不安全、但包 getter/setter 又太囉唆」的兩難：

```csharp
public string Name {
    get { return name; }
    set { name = value; }
}
```

- **Delegate**：型別安全的函數指標。C 語言的函數指標只有一個位址、毫無型別檢查；delegate 則把「方法的簽名」變成型別的一部分：

```csharp
delegate int Op(int a, int b);
Op add = (a, b) => a + b;   // C# 3.0 的 lambda 語法
```

**第三，取捨的哲學。** Java 當年「為了安全幾乎拿掉一切」：沒有指標、沒有運算子多載、沒有無號整數。Hejlsberg 的推理是：**開發者是大人，給他們武器但加上保險。** 所以 C# 有運算子多載、有 unsafe 區塊可以寫指標、有 unsigned 整數——但這些危險能力都被明確標記出來。

## 結案報告

C#/.NET 的遺產極為深遠：

1. **多語言 VM 成為主流設計。** CLR 證明了虛擬機可以是語言中立的基礎設施。這條思路直接影響了後來的 JVM 生態（Scala、Kotlin）、以及 LLVM 工具鏈「任何前端、任何後端」的架構（見 [2014-Swift.md](2014-Swift.md)）。
2. **C# 本身持續演化**，從 C# 3.0 的 LINQ（把查詢內建進語言，融合函數式思維）、async/await（Hejlsberg 團隊的發明，後被 JavaScript、Python、Rust 全部抄走）、到 record 型別與模式匹配。有趣的是，C# 與 Java 展開了長達二十年的「互抄大賽」：C# 先有屬性，Java 後補 record；Java 先有 lambda 編譯困境，C# 的表達式樹則提供了另一種解法。
3. **.NET Core 的開源與跨平台**（2016 年起）：微軟最終承認「Windows-only」是錯的，把 .NET 開源、重寫核心、跨到 Linux 與 macOS。2014 年 Satya Nadella 上任後的「Microsoft loves Linux」，正是這場轉型的政治句點。.NET Core 合併回 .NET 5 之後，微軟完成了當年 Sun 用 Java 想做的事——只不過用的是自己當年抄來的藍圖。

諷刺的是歷史的輪迴：微軟當年因為破壞 Java 跨平台被告，二十年後靠著開源跨平台贏回開發者的心。VM 時代的第二張王牌，就這樣打出去了。

## 證據與工具

以下用 C# 展示 property、delegate 與 LINQ 三大遺產：

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

class Student {
    public string Name { get; set; }      // property
    public int Score { get; set; }
}

class Program {
    static void Main() {
        var students = new List<Student> {
            new Student { Name = "Amy",  Score = 90 },
            new Student { Name = "Bob",  Score = 60 },
            new Student { Name = "Carl", Score = 75 },
        };

        // LINQ：函數式查詢內建於語言
        var passed = students
            .Where(s => s.Score >= 70)
            .OrderBy(s => s.Score)
            .Select(s => s.Name);

        foreach (var name in passed) Console.WriteLine(name);
        // Amy, Carl

        // delegate：型別安全的函數指標
        Func<int, int, int> max = Math.Max;
        Console.WriteLine(max(3, 7));  // 7
    }
}
```

再用 Python 模擬 CLR 的「CIL → 堆疊機執行」核心機制，展示中間語言如何驅動虛擬機：

```python
# 模擬一個極簡的 CLR：棧式 VM 執行 CIL 指令
def run_cil(instructions):
    stack = []
    output = []
    for op, *args in instructions:
        if op == "ldc.i4":      # 推入常數
            stack.append(args[0])
        elif op == "add":       # 彈出兩值相加
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif op == "mul":
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        elif op == "print":     # 模擬 Console.WriteLine
            output.append(stack.pop())
        elif op == "sub":
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
    return output

# (3 + 4) * 2 的 CIL
program = [
    ("ldc.i4", 3),
    ("ldc.i4", 4),
    ("add"),
    ("ldc.i4", 2),
    ("mul"),
    ("print"),
]
print(run_cil(program))  # [14]
```

這個小小的模擬器道出了 VM 時代的本質：**語言編譯成中間語言，中間語言驅動堆疊機**。無論寫程式的是 C#、F# 還是 IronPython，最終都在同一條流水線上相遇——這就是 Hejlsberg 在 2000 年埋下的種子。
