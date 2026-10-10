# 1995 — Java 與 JVM 的誕生

## 案件摘要
1995 年 5 月，Sun Microsystems 發表 Java 語言與 JVM（Java Virtual Machine）。兇手不是來自學術殿堂，而是來自「機上盒」這個失敗的消費性產品。Oak 計畫死於硬體市場，卻在網頁時代復活，用「位元組碼 + 虛擬機」徹底改寫了軟體的發行方式。

## 前因 -- 為什麼會有這個案子
- **硬體碎片化之痛**：1990 年代初，嵌入式裝置（機上盒、電視、PDA）晶片架構五花八門（x86、ARM、PowerPC、SPARC），C/C++ 編譯出的機器碼無法跨平台。
- **Green Project（1991）**：James Gosling、Mike Sheridan、Patrick Naughton 受命開發下一代機上盒技術，Gosling 寫了名為 **Oak** 的新語言。
- ** Oak 的失敗與轉機**：機上盒標案被 Time Warner 招標後流標，Oak 產品無商業價值。恰在此時，1993 年 Mosaic 瀏覽器引爆網頁時代——Internet 上千萬台異質電腦，正是 Oak 需要的「碎片化平台」。
- **歷史線索**：跨平台虛擬機的构想早有先例——1970 年代 UCSD Pascal 的 p-code、IBM 的 VM/370，但都未在大眾市場成功。Oak 團隊把「小型堆疊式位元組碼 VM」帶進了網頁。

## 線索與推理 -- 數學式、程式、理論

### JVM 架構四要素
1. **Class Loader**：動態載入 `.class` 檔，形成命名空間隔離（後來成為安全模型的基礎）。
2. **Bytecode**：平台中立的指令集，存於 `.class` 檔中。
3. **直譯器 / 執行引擎**：逐條執行位元組碼（早期版本純直譯）。
4. **GC（垃圾回收）**：自動記憶體管理，免除 C 的 `malloc/free` 與懸空指標。

### 堆疊式位元組碼
JVM 是**堆疊式機器**（stack machine）：運算元隱含在運算堆疊上，指令不需編碼暫存器位址，因此位元組碼極為緊緻。例如 Java 方法：

```java
int one() { return 1; }
```

編譯成：

```
iconst_1   // 將常數 1 推入運算堆疊
ireturn    // 從堆疊彈出 int 並返回給呼叫者
```

形式化地，堆疊機的單步轉移關係可寫成：

$$
\langle c \cdot \mathit{code},\ S,\ F \rangle \;\longrightarrow\; \langle \mathit{code}',\ S',\ F' \rangle
$$

其中 $S$ 為運算堆疊、$F$ 為框架（frame，含區域變數）。例如 `iconst_1` 的語義：

$$
\langle \mathtt{iconst\_1} :: \mathit{code},\ S,\ F\rangle \to \langle \mathit{code},\ 1 :: S,\ F\rangle
$$

### Write Once Run Anywhere
編譯一次、到處執行的承諾來自一個簡單的分層：

$$
\text{Java 原始碼} \xrightarrow{\text{javac}} \text{Bytecode} \xrightarrow{\text{各平台 JVM}} \text{原生機器碼}
$$

平台的差異被 JVM 吸收，位元組碼成為通用的「中介表示」（IR）。數學上，這是让編譯器的 $n \times m$ 問題（$n$ 種語言 × $m$ 種平台）降為 $n + m$ 問題。

### Java Applet 與網頁時代
1995 年 Netscape Navigator 1.1 內嵌 JVM，`<applet>` 標籤讓網頁能執行互動程式。Applet 伴隨**沙箱（sandbox）安全模型**：bytecode 經過 verifier 驗證（不可偽造指標、不可越權存取），才能執行。這是第一次，數百萬普通使用者在他們的電腦上執行「來自陌生伺服器」的程式。

### Python 實作簡單 JVM 式堆疊 VM
以下用 Python 實作一個能執行 Java 風位元組碼的堆疊 VM：

```python
class JVM:
    def __init__(self, code):
        self.code = code          # 位元組碼列表
        self.pc = 0               # 程式計數器
        self.stack = []           # 運算堆疊

    def push(self, v): self.stack.append(v)
    def pop(self): return self.stack.pop()

    def run(self):
        while self.pc < len(self.code):
            op = self.code[self.pc]; self.pc += 1
            if op == 'iconst_1':   self.push(1)
            elif op == 'iconst_2': self.push(2)
            elif op == 'iadd':     self.push(self.pop() + self.pop())
            elif op == 'imul':     self.push(self.pop() * self.pop())
            elif op == 'ireturn':  return self.pop()
            else: raise ValueError(f"unknown opcode: {op}")

# 對應 Java: int f() { return 1 + 2 * 3; }
# javac 會產生: iconst_2 iconst_3 imul iconst_1 iadd ireturn
code = ['iconst_2', 'iconst_3', 'imul', 'iconst_1', 'iadd', 'ireturn']
print(JVM(code).run())   # 輸出 7
```

注意堆疊機如何自然地表達運算樹的後序走訪：`2 * 3` 先完成，`1 +` 後套用——這正是 JVM 位元組碼的設計精髓。

## 結案 -- 後果與影響
- Java 成為 2000 年代企業後端（J2EE/Servlet）與 Android（2008 起，Dalvik/ART 皆執行 Java 位元組碼變體）的霸主語言。
- 「VM + 位元組碼 + GC」成為新語言的標準配方：C#/.NET CLR（2002）直接對標 JVM。
- Applet 雖已死亡（2018 移除），但它的 sandbox 與 verifier 概念延續到今日的瀏覽器安全模型。
- 1995 年之後，「編譯目標」不再只有 CPU——JVM、CLR、WASM（2017）都是虛擬機目標。

## 關鍵人物與文獻
- **James Gosling**：Java 之父，Oak 的設計者。
- **Bill Joy**：Sun 共同創辦人，促成 Oak 轉型 Java。
- **Arthur van Hoff**：早期 JVM 實作關鍵工程師。
- Gosling, J. & McGilton, H., *The Java Language Environment*（1996, Sun 白皮書）。
- Lindholm, T. et al., *The Java Virtual Machine Specification*（1997 初版）。
- 先例文獻：Popek & Klawe, *The Case for A*, or p-code（1975）；UCSD Pascal p-System（1978）。
