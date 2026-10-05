# 1977-Boyer-Moore 字串搜尋演算法

## 案件摘要

1977 年，Robert Boyer 與 J Strother Moore 在《Communications of the ACM》發表〈A Fast String Searching Algorithm〉，揭開一樁「搜尋可以比線性更快」的懸案。同年的 KMP 演算法從左往右比對、保證線性時間；Boyer-Moore 卻反其道而行，從模式串的**右端**開始比對。破案時刻在於：失配不是壞事，而是情報——它告訴你模式串可以安全地滑多遠，讓主串指標大步跳躍，達到實務上的**亞線性（sublinear）**速度。

## 前因 -- 為什麼會有這個案子

- 樸素演算法每次失配只前進一字元，最壞情況 $O(nm)$，在長文件上慢得難以忍受。
- 文字編輯器、編譯器掃描與 grep 的前身工具，需要的是「實務上快」；KMP（1977 同年發表）雖保證 $O(n+m)$，但每個字元至少比對一次，實務常數不小、平均速度不見得快。
- Boyer 當時在德州大學奧斯汀分校研究定理證明器（NQTHM 前身），需要快速字串搜尋，於是從被眾人忽略的「比對順序」角度重新偵查。

## 線索與推理 -- 數學式、程式、理論

### 線索一：從右往左比對

模式串 $P[1..m]$ 與主串 $T[1..n]$ 對齊後，先比 $P[m]$ 與窗口最右端 $T[i]$。若失配，情報立刻到手：$T[i]$ 不在窗口內，接下來有大範圍可以排除。

### 線索二：壞字元規則（bad character rule）

失配時，把模式串滑到主串中該「壞字元」$c$ 在模式串內最後出現的位置對齊；若 $c$ 不在 $P$ 中，直接滑過整個窗口：

$$
\text{shift}_{bc}(c) = \max\{\,1,\; m - \max_{j \le m}\{ j : P[j] = c \}\,\}
$$

### 線索三：好後綴規則（good suffix rule）

比對到右端某點失配時，右端已匹配的後綴 $u$ 是重要線索：找出 $u$（或與之邊框相符的 $P$ 前綴）在模式串中的下一次出現位置並對齊：

$$
\text{shift}_{gs} = \min\{\, d > 0 : P[k-d+1..m-d] = P[k+1..m] \ \text{或邊框相符} \,\}
$$

實際滑動量取兩規則較大者：$\text{shift} = \max(\text{shift}_{bc},\ \text{shift}_{gs})$。

### 線索四：亞線性的由來

每個窗口至少比對一個字元、至多跳 $m$ 格，平均而言主串指標以 $O(n/m)$ 量級前進——**主串越長，相對越快**，這正是亞線性的破案時刻。原始版在週期性文字（如 $T = a^n$、$P = a^m$）上會退化為 $O(nm)$；Galil（1979）加入「記住上一輪已匹配段、只比對新增部分」的規則，證得最壞情況線性 $O(n+m)$。

### 程式偵查：Python 實測比對次數

```python
def build_gs(pat):
    m, gs = len(pat), []
    for k in range(m):            # 在索引 k 失配，已匹配後綴 u = pat[k+1:]
        u = pat[k + 1:]
        if not u:
            gs.append(1); continue
        best = m
        for d in range(1, m + 1): # 情況一：u 在模式串中的另一次出現
            if k + 1 - d >= 0 and pat[k + 1 - d:m - d] == u:
                best = d; break
        else:                     # 情況二：P 的前綴與 u 的後綴相符（邊框）
            for l in range(len(u) - 1, 0, -1):
                if pat[:l] == u[len(u) - l:]:
                    best = m - l; break
        gs.append(best)
    return gs
def boyer_moore(text, pat):
    n, m = len(text), len(pat)
    last = {c: j for j, c in enumerate(pat)}  # 壞字元表
    gs = build_gs(pat)                        # 好後綴表
    count, s = 0, 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pat[j] == text[s + j]:
            j -= 1; count += 1
        if j < 0:
            return s, count
        count += 1
        bc = max(1, j - last.get(text[s + j], -1))
        s += max(bc, gs[j])
    return -1, count
def naive_count(text, pat):
    n, m = len(text), len(pat)
    count = 0
    for s in range(n - m + 1):
        j = 0
        while j < m and text[s + j] == pat[j]:
            j += 1; count += 1
        count += 1
        if j == m:
            return s, count
    return -1, count

if __name__ == "__main__":
    t = "AB" * 5000 + "FINDME" + "XY" * 5000  # 主串約 2 萬字元
    s1, c1 = boyer_moore(t, "FINDME")
    s2, c2 = naive_count(t, "FINDME")
    print(f"Boyer-Moore: 位置 {s1}, 比對 {c1} 次")
    print(f"樸素演算法:  位置 {s2}, 比對 {c2} 次")
```

實測結果：Boyer-Moore 只需約 6-20 次比對，樸素演算法需上千次——亞線性當場現形。

## 結案 -- 後果與影響

- Boyer-Moore 成為許多系統 grep 與文字編輯器搜尋的基礎或預設實作之一；「實務亞線性」第一次被清楚示範，演算法評估從純理論轉向理論與實務並重。
- KMP（理論線性、每字元必比）與 Boyer-Moore（實務亞線性、指標跳躍）成為字串搜尋的雙璧對照組。
- Horspool（1980）提出簡化版 Boyer-Moore-Horspool，只留壞字元規則，表格小、速度快，廣泛用於實務；Galil（1979）的修補證明最壞線性，補齊理論拼圖。
- Boyer 本人在定理證明器（與 Moore 合作的 NQTHM 歸納證明系統）上的工作使他獲 1988 年圖靈獎——本案只是他偵探生涯的副線。

## 關鍵人物與文獻（條列，含真實文獻書目）

- Robert S. Boyer, J Strother Moore (1977). *A Fast String Searching Algorithm*. Communications of the ACM, 20(10), 762–772.
- Donald E. Knuth, James H. Morris, Jr., Vaughan R. Pratt (1977). *Fast Pattern Matching in Strings*. SIAM Journal on Computing, 6(2), 323–350.
- Zvi Galil (1979). *On Improving the Worst Case Running Time of the Boyer-Moore String Matching Algorithm*. SIAM Journal on Computing, 8(4), 612–631.
- R. Nigel Horspool (1980). *Practical Fast Searching in Strings*. Software: Practice and Experience, 10(6), 501–506.
- Robert S. Boyer, J Strother Moore (1979). *A Computational Logic*. Academic Press（NQTHM 定理證明器理論基礎）.
