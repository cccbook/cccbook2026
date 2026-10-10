# 1854 - Boole 邏輯代數（讓推理變成算術）

## 案件摘要
1854 年，George Boole 發表 *An Investigation of the Laws of Thought*：
建立**布爾代數**——把邏輯推理寫成代數運算：
$$\neg x \in \{0,1\}, \qquad x \land y = x\cdot y, \qquad x \lor y = x+y-x\cdot y.$$
$$\text{（NOT, AND, OR）} = \text{（1−x, xy, x+y−xy）}.$$
**邏輯 = 代數**。此後 60 年，開關代數、邏輯閘、二進位加法器、二進位算術，
全部是布爾代數的電路實現：
$$\text{Boole（1854）} \xrightarrow{\text{Shannon 1938}} \text{開關代數} \xrightarrow{\text{1947}} \text{邏輯閘} \xrightarrow{\text{1971}} \text{CPU 算術單元}.$$

## 前因 -- 為什麼會有這個案子
- **19 世紀的邏輯困境**：傳統邏輯（亞里士多德的命題邏輯）不能做「代數」——
  無法像數字一樣加減乘除、求解方程。**邏輯不可計算**。
- **背景革命**：Babbage 的分析機（見「1837-Babbage差分機.md」）需要「條件判斷」，
  Ada Lovelace 認識到：**邏輯運算若能代數化，就能在機器上執行**。
  **但 1843 年還沒有這樣的代數**——這是 Boole 補上的缺口。
- **Boole 的偵探直覺（化繁為簡的哲學）**：把邏輯思維看成「集合運算」：
  - 「A 且 B」= A ∩ B（交集）→ **乘積**（用 0/1 表示集合成員）
  - 「A 或 B」= A ∪ B（聯集）→ **加法**（$x+y-xy$ 去重）
  - 「非 A」= A 的補集 → **減法**（$1-x$）
  布爾在 *laws of thought* 中寫道：「邏輯的推理形式就是代數運算的形式」。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：布爾代數的四條基本律
布爾代數 $(\{0,1\},\ \lor,\ \land,\ \neg,\ 0,\ 1)$ 滿足：
1. **交換律**：$x\lor y = y\lor x,\ \ x\land y = y\land x$
2. **結合律**：$(x\lor y)\lor z = x\lor(y\lor z)$
3. **分配律**：$x\land(y\lor z) = (x\land y)\lor(x\land z)$
4. **吸收律**：$x\lor(x\land y) = x$
5. **互補律**：$x\lor\neg x = 1,\ \ x\land\neg x = 0$
6. **冪等律**：$x\land x = x,\ \ x\lor x = x$

只需 0、1 兩個元素，就能完整表示邏輯。**代數結構定義了邏輯計算**。

### 第二條線索：布爾代數中的環（GF(2)）
若把 $\lor$ 視為 **XOR**（模 2 加法），則布爾代數就是 $\mathbb{F}_2 = \mathbb{Z}/2\mathbb{Z}$：
$$x \oplus y = (x+y) \bmod 2, \qquad x \land y = x\cdot y.$$
- 這就是 **GF(2)（二進位有限域）**——今日 Galois Field 數位訊號處理的基礎。
- **XOR 門是算術的靈魂**：加法器的進位 = XOR，檢錯碼 = XOR 校驗。

### 第三條線索：表達式的簡化（邏輯最小化）
任何布林函數可用**真值表 + Karnaugh 圖**化簡為最小 SOP（和項積）：
$$f(x,y) = \bar{x}y + x\bar{y} = x \oplus y \quad \text{（XOR，需 4 閘）}.$$
- 電路最小化直接決定了**晶片面積與功耗**——今日EDA（IC 設計軟體）的核心任務。
- 例：多數決（majority）：
  $$f(a,b,c) = ab + ac + bc \quad \text{（3 個 AND + 2 個 OR + 1 個 NOT）}.$$

### Python：布爾代數與邏輯閘的關係

```python
def xor(a,b):    return (a+b) % 2
def and_(a,b):   return a*b
def or_(a,b):    return a|b          # a+b-ab
def not_(a):     return 1-a

# 半加器（Half Adder）——最簡單的算術電路
def half_adder(a, b):
    s = xor(a, b)      # 和：XOR
    c = and_(a, b)     # 進位：AND
    return s, c

def full_adder(a, b, cin):
    s1, c1 = half_adder(a, b)
    s2, c2 = half_adder(s1, cin)
    cout  = or_(c1, c2)
    return s2, cout

# 二進位加法器（用全加器串接）
def add_binary(x, y):
    result, carry, i = 0, 0, 0
    while x or y or carry:
        bx, by = (x>>i)&1, (y>>i)&1
        bit, carry = full_adder(bx, by, carry)
        result |= bit << i
        i += 1
    return result

for a,b in [(0,0),(0,1),(1,0),(1,1)]:
    print(f"HalfAdder({a},{b}) = sum {xor(a,b)}, carry {and_(a,b)}")
print("3+5 =", add_binary(3,5), "(=8)")
print("7+1 =", add_binary(7,1), "(=8，驗證進位鏈)")
print("10+7 =", add_binary(10,7), "(=17)")
```
輸出：
```
HalfAdder(0,0) = sum 0, carry 0
HalfAdder(0,1) = sum 1, carry 0
HalfAdder(1,0) = sum 1, carry 0
HalfAdder(1,1) = sum 0, carry 1
3+5 = 8 (=8)
7+1 = 8 (=8，驗證進位鏈)
10+7 = 17 (=17)
```
（半加器用 XOR（和）與 AND（進位）——兩個閘就完成二進位加法的核心——
**整個 CPU 的算術單元都是由布爾閘堆疊的**。）

## 結案 -- 後果與影響
- **Shannon（1938）的開關代數**：Claude Shannon 證明**布爾代數可直接應用於繼電器開關電路**——
  「任何邏輯運算都可以用電開關實現」。這是**邏輯代數 → 電子電路**的橋接。
- **電腦電路的基礎語言**：NOT/AND/OR/XOR/NAND/NOR/XNOR 閘 → 加法器 → ALU → CPU → 記憶體。
  **今日一顆數十億電晶體的晶片，全部是布爾代數的電路實現**。
- **硬體描述語言（HDL）**：Verilog/VHDL（1980s）——**用「類 C」語言描述布爾代數電路**：
  數位設計師寫 HDL，EDA 綜合成電閘級電路。
- **形式化驗證與 SAT 求解器**：今日晶片驗證使用 SAT/SMT 求解器（SAT 問題 $\exists$ 滿足某公式的賦值）——
  **求解布爾公式 = 1854 年的核心問題**。
- **軟體工程工具**：靜態分析（static analysis）、程式驗證（verification）、編譯器優化——
  都基於**布爾代數**。
- 歷史定位：**Boole 一本形而上學著作《思考的法則》，意外打通了數學、邏輯、電路、電腦四者**——
  今日數位世界 100% 的運算規則，就是布爾代數。

## 關鍵人物與文獻
- **G. Boole**：*An Investigation of the Laws of Thought* (1854)。
- **C. Shannon**：〈A Symbolic Analysis of Switching Circuits〉(1938)——開關代數。
- **T. De Morgan**：De Morgan 定理 (1846)—— $|, \&, \neg$ 轉換。
- 相關案件：`1837-Babbage差分機.md`、`1936-Turing機.md`、`1947-電晶體.md`、`1971-Intel4004微處理器.md`。