# 1967 Simula 67：排隊系統催生物件導向

## 案發現場

1960 年代初，挪威計算中心（Norwegian Computing Center, NCC）接下一批很特別的案子：核電廠要模擬反應爐的安全程序、港口要模擬船隻進出的作業排程、銀行要模擬櫃檯排隊的人潮、航空公司要模擬訂位系統。這些問題有個共同名字——**離散事件模擬（discrete event simulation）**：系統由各種「實體」（船、顧客、機器）組成，實體在時間軸上互動、排隊、搶資源。

遇見這個問題的是 NCC 的兩位研究員：Ole-Johan Dahl 與 Kristen Nygaard。他們先用 ALGOL 60（見 [1958-ALGOL.md](1958-ALGOL.md)）的 SIMULA I 版本做模擬，卻撞上一堵牆：ALGOL 的區塊結構在模擬中完全不夠用。問題的核心推理如下——一艘船和一個顧客都是「實體」，都有屬性（載重、姓名）、都有行為（進港、排隊），但 ALGOL 的程序（procedure）只能描述行為不能封裝屬性；更致命的是，**實體的生命週期比區塊長**：ALGOL 的變數離開 `begin/end` 就消失，可是一艘船在模擬結束前必須一直活著。如何讓「資料」與「行為」綁在一起、並且活得比作用域更久？1967 年，Dahl 與 Nygaard 在 SIMULA 67 中給出了答案：**class（類別）**。這一個概念，後來被稱為物件導向程式設計（OOP）的誕生。

## 偵查過程

### 線索一：class——把記錄與程序縫合在一起

Simula 67 的關鍵靈感來自一個簡單的合併推理：ALGOL 60 已經有兩種「描述工具」——record 式的資料宣告與 procedure 式的行為宣告；Nygaard 推導出：**把兩者合併成一個語法單位**，就得到 class：

```simula
begin
    class SHIP;
        integer LOADED;
    begin
        procedure ENTER_PORT;
        begin
            LOADED := LOADED - 10;
            outtext("船已進港")
        end ENTER_PORT;
    end SHIP;
    ref(SHIP) theShip;
    theShip :- new SHIP;
    theShip.LOADED := 100;
    theShip.ENTER_PORT
end
```

注意這個推理鏈。第一，`SHIP` 類別同時封裝了屬性 `LOADED` 與程序 `ENTER_PORT`——資料與行為第一次縫合在同一個語法單位裡。第二，`new SHIP` 在**堆積（heap）**上配置物件，而不是在執行堆疊上——這直接解決了「實體必須活得比區塊久」的問題；物件的生命週期由引用（`ref(SHIP)`）控制，離開作用域後物件仍然活著。第三，`theShip.LOADED` 的點號存取語法，成為後世所有物件導向語言的標準記法。

### 線索二：繼承與虛擬程序——從「複製貼上」到「擴充」

模擬的需求進一步推導出第二個概念。港口模擬中，船隻有油輪、貨輪、客輪，它們九成的程式碼相同（都要進港、排隊），只有少數行為不同（裝卸方式不同）。Dahl 的推理是：與其複製貼上，不如讓新類別**繼承**舊類別的全部屬性與程序，再擴充或覆寫差異的部分：

```simula
class SHIP;
    integer LOADED;
begin
    procedure DOCKING;
        outtext("一般靠港");
end;

SHIP class TANKER;
begin
    procedure DOCKING;
        outtext("油輪需特殊碼頭");
end;

ref(SHIP) s;
s :- new TANKER;      ! s 是 SHIP 引用，但實際指向 TANKER;
s.DOCKING             ! 執行時期才決定呼叫哪個 DOCKING -> 虛擬程序;
```

`SHIP class TANKER` 語法宣告 TANKER 繼承 SHIP 的所有成員。而 `DOCKING` 這種**虛擬程序（virtual procedure）**的推理是關鍵：`s` 的靜態型別是 `ref(SHIP)`，但實際指向 `TANKER` 物件——呼叫 `s.DOCKING` 時該執行哪個版本？Simula 的答案是：**在執行時期根據物件的實際型別動態決定**。這正是動態繫結（dynamic binding）/多型（polymorphism）的誕生時刻，後世 C++ 的 `virtual` 關鍵字與虛擬函數表（vtable）直接承襲自 Simula。

### 線索三：協同程序——模擬的時間軸推理

模擬還有一個更深的需求：多個實體的行為要「同時」在時間軸上交錯進行。Simula 借鑑了協同程序（coroutine）概念——物件可以暫停自己的執行、讓別的物件執行、稍後再恢復。這個「暫停—恢復」的推理模型，正是模擬排隊系統（顧客到櫃檯→等待→服務→離開）的自然表達方式，也是後世生成器、async/await 的理論先聲。

## 結案報告

Simula 67 是一個「商業上失敗、概念上稱王」的經典：它沒有流行起來（挪威計算中心的編譯器太慢、推廣有限），但它播下的概念種子長成了整個物件導向森林：

- **Smalltalk**：1970 年代 Xerox PARC 的 Alan Kay 直接承認 Simula 是 Smalltalk 的主要靈感來源，並把「物件」推向極致——「一切皆物件」、訊息傳遞、圖形化介面。Kay 更創造了「object-oriented」這個詞。
- **C++**：1979 年 Bjarne Stroustrup 在劍橋做博士研究時接觸了 Simula，深受其類別與繼承概念吸引，回到貝爾實驗室後在 C 之上加上 Simula 式的類別，命名為「C with Classes」，即 C++ 的前身。C++ 的 `class`、`virtual`、建構子/解構子，全部源於 Simula。
- **Java、C#、Python、Ruby**：整個 1990 年代之後的主流語言都內建類別與繼承，OOP 成為軟體工業的預設典範——設計模式（GoF）、UML、敏捷方法，都建築在 Simula 播下的概念上。
- **協同程序**的遺產：生成器（Python 的 `yield`）、Go 的 goroutine、JavaScript/Python 的 async/await，都是「暫停—恢復」模型的現代化身。

一句話總結：FORTRAN 給了世界公式，COBOL 給了世界英文，ALGOL 給了世界文法——而 Simula 在挪威的港口與銀行排隊模擬中，給了世界「物件」。

## 證據與工具

以下用 Python 重現 Simula 67 的 class、繼承、虛擬程序與排隊模擬：

```python
import random

# 模擬 Simula 的 class：屬性 + 程序縫合在同一個單位
class Ship:
    def __init__(self, loaded):          # 相當於 Simula 的物件初始化
        self.loaded = loaded
    def docking(self):                    # 虛擬程序：子類別可覆寫
        return "一般靠港"
    def enter_port(self):
        self.loaded -= 10
        return f"{type(self).__name__} 進港，卸貨後載重 {self.loaded}"

# 繼承：SHIP class TANKER -> 子類別擴充父類別
class Tanker(Ship):
    def docking(self):                    # 覆寫虛擬程序 -> 動態繫結
        return "油輪需特殊碼頭"

# 多型驗證：SHIP 引用，執行時期才決定呼叫哪個 DOCKING
fleet = [Ship(100), Tanker(200), Ship(150)]
for s in fleet:
    print(s.docking(), "|", s.enter_port())

# 離散事件排隊模擬（Simula 誕生的原初需求）：單櫃台銀行
def bank_simulation(n_customers, mean_service=5.0):
    """顧客依序到達，單一櫃台服務，計算平均等待時間"""
    clock, waiting = 0.0, []
    queue_end = 0.0                       # 櫃台何時空出來
    for i in range(n_customers):
        arrive = clock + random.expovariate(1 / 3.0)   # 到達間隔 ~ Exp(1/3)
        service = random.expovariate(1 / mean_service) # 服務時間 ~ Exp(1/5)
        start = max(arrive, queue_end)                 # 排隊：等櫃台空出
        wait = start - arrive
        waiting.append(wait)
        queue_end = start + service                    # 物件佔用資源，時間推進
        clock = arrive
    return sum(waiting) / len(waiting)

print(f"\n1000 位顧客的平均等待時間: {bank_simulation(1000):.2f} 分鐘")

# 協同程序（暫停-恢復）模型：Python 的 yield 是其現代化身
def customer_life():
    for step in ["到達銀行", "排隊等待", "櫃台服務", "離開"]:
        yield step                       # 暫停，讓模擬時鐘推進，稍後恢復

life = customer_life()
print("協同程序: ", next(life), "->", next(life), "->", next(life))
```

執行結果顯示四件事：第一，`Ship` 類別把屬性與程序縫合；第二，`Tanker` 繼承並覆寫 `docking`，迴圈以 `SHIP` 引用遍歷時，執行時期才決定呼叫哪個版本——正是虛擬程序的動態繫結；第三，排隊模擬計算出平均等待時間，這是 1960 年代挪威計算中心接下的原初案件；第四，`yield` 生成器重現了協同程序「暫停—恢復」的時間軸推理。這個排隊模擬的需求，最終催生了物件導向程式設計。
