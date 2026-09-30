# 1936 - Turing 機與停機問題

## 案件摘要
1936 年，23 歲的 Turing 發表《論可計算數及其在判定問題上的應用》，發明圖靈機這個「理想化的人類計算者」模型，構造出通用圖靈機，並用對角線法證明停機問題不可判定——一舉解決了 Hilbert 的判定問題，也埋下了通用電腦的種子。

## 前因 -- 為什麼會有這個案子
Hilbert 的判定問題（Entscheidungsproblem）懸而未決：「是否存在機械程序判定任意命題的有效性？」Church (1936) 已用 λ 演算給出否定答案，但 λ 演算過於抽象，「它就是所有有效計算」這點缺乏直覺支撐。Turing 要找一個**直觀到無可辯駁**的計算模型——他觀察「人類用紙筆計算」的過程：一個人在紙帶上寫符號、盯著看、按規則改寫、移動位置——圖靈機就此誕生。

## 線索與推理 -- 數學式、程式、理論

### 圖靈機的定義
一個圖靈機是七元組 $M = (Q, \Gamma, \Sigma, \delta, q_0, \sqcup, F)$：

- $Q$：有限狀態集
- $\Gamma$：紙帶字母集（含空白符 $\sqcup$）
- $\Sigma \subseteq \Gamma$：輸入字母集
- $\delta$：轉移函數，這是機器的「程式」：
$$\delta(q, a) = (q', b, D)$$
（在狀態 $q$ 讀到符號 $a$ 時：寫入 $b$、轉到狀態 $q'$、讀寫頭移動 $D \in \{L, R\}$）
- $q_0 \in Q$：起始狀態；$F \subseteq Q$：接受狀態集

無限紙帶 + 有限控制 + 機械規則 = 一切「有效計算」的極限模型。

### 通用圖靈機（Universal Turing Machine）
Turing 的神來之筆：圖靈機的「程式」$\delta$ 本身可以被編碼為一個字串（Gödel 編碼，見 `1931-Godel不完備定理.md`），於是可以造一台**模擬任何圖靈機**的機器：

$$U(\ulcorner M \urcorner, x) = M(x)$$

$U$ 讀入「機器 $M$ 的編碼」與「輸入 $x$」，就照 $M$ 的規則在紙帶上模擬執行。**這就是現代電腦的理論原型**——軟體（$\ulcorner M \urcorner$）與硬體（$U$）分離，一台機器跑所有程式。

### 停機問題不可判定
**定義**：停機問題是集合

$$\mathrm{HALT} = \{ (\ulcorner M \urcorner, x) \mid M(x) \text{ 在有限步內停機} \}$$

**定理**：HALT 不可判定（不存在圖靈機判定所有輸入是否停機）。

**對角線證明**（反證法）：假設存在判定機 $H$，使得 $H(M, x) = \text{true}$ 當且僅當 $M(x)$ 停機。構造對角機：

$$D(M) = \begin{cases} \text{不停機} & \text{若 } H(M, M) = \text{true（即 } M(M) \text{ 停機）} \\ \text{停機} & \text{若 } H(M, M) = \text{false} \end{cases}$$

一言以蔽之：$D(M) = \neg M(M, x)$——**與自己對著幹**。現在問：$D(D)$ 停機嗎？

- 若 $D(D)$ 停機，依 $D$ 的定義需 $H(D, D) = \text{false}$，即 $D(D)$ **不**停機 → 矛盾。
- 若 $D(D)$ 不停機，依定義需 $H(D, D) = \text{true}$，即 $D(D)$ 停機 → 矛盾。

兩難。故 $H$ 不存在，HALT 不可判定。$\blacksquare$

**偵探筆記**：這與 Gödel 的 $G \leftrightarrow \neg\mathrm{Prov}(\ulcorner G\urcorner)$ 是同一招——**對角線自我指涉**。Gödel 讓句子否定自己的可證明性，Turing 讓程式否定自己的可判定性。

### 判定問題的解決
由停機問題歸約到判定問題：給定一階公式 $\varphi$，可以機械地構造一個圖靈機 $M_\varphi$ 搜索 $\varphi$ 的反例模型（利用 Löwenheim–Skolem 定理，只需搜可數模型，見 `1913-LowenheimSkolem定理.md`）：

$$\models \varphi \iff M_\varphi \text{ 不停機}$$

若判定問題可解，則 HALT 可解——矛盾。故**一階邏輯有效性不可判定**（Church–Turing 定理）。Hilbert 的第三大問題就此終結。

### 程式碼：Python 模擬一個簡單圖靈機
模擬一台「二進制加一」圖靈機：輸入如 `1011`，輸出 `1100`。

```python
class TuringMachine:
    def __init__(self, delta, start, blank, accept):
        self.delta, self.start = delta, start
        self.blank, self.accept = blank, accept

    def run(self, tape, max_steps=10000):
        tape = {i: ch for i, ch in enumerate(tape)}
        head, state, steps = 0, self.start, 0
        while state not in self.accept and steps < max_steps:
            sym = tape.get(head, self.blank)
            if (state, sym) not in self.delta:
                return None, steps        # 卡住 = 非正常停機
            new_state, write, move = self.delta[(state, sym)]
            tape[head] = write
            head += 1 if move == 'R' else -1
            steps += 1
        return (''.join(tape.get(i, self.blank)
                        for i in range(min(tape), max(tape) + 1)).strip(self.blank)
                if state in self.accept else None), steps

# 二進制加一：從最右端往左找第一個 0，改成 1，其後的 1 全改成 0
delta = {
    ('q0', '0'): ('q0', '0', 'R'), ('q0', '1'): ('q0', '1', 'R'),
    ('q0', ' '): ('q1', ' ', 'L'),                # 到尾端，回頭
    ('q1', '1'): ('q1', '0', 'L'),                # 進位：1 變 0，繼續左移
    ('q1', '0'): ('acc', '1', 'N'),               # 找到 0，改 1，停
    ('q1', ' '): ('acc', '1', 'N'),               # 全是 1 -> 進位成新位
}
tm = TuringMachine(delta, 'q0', ' ', {'acc'})
print(tm.run('1011'))   # ('1100', 7)  -> 1011 + 1 = 1100 ✓
print(tm.run('111'))    # ('1000', 7)  -> 111 + 1 = 1000 ✓
```

```python
# 停機問題的「偽解」與其不可能性
def H(M, x):          # 假設的停機判定器
    """這個函數無法被真正實作——這正是定理的內容！"""
    raise NotImplementedError("HALT 不可判定！")

def D(M):
    try:
        H(M, M)       # 檢查 M(M) 是否停機
        while True:   # 若停機 -> 我就不停機
            pass
    except NotImplementedError:
        return        # 若不停機 -> 我就停機

# D(D) 停機嗎？兩難 -> H 不可能存在。
# Python 有 sys.setrecursionlimit、timeouts 等經驗性手段，
# 但沒有任何「完美」的停機判定器——這是數學事實，不是工程限制。
```

## 結案 -- 後果與影響
- **判定問題終結**：Church–Turing 定理證明一階邏輯有效性不可判定；Hilbert 綱領的最後支柱倒塌。
- **不可判定性的譜系**：此後大量問題被證明不可判定（停機問題歸約是標準工具）：Post 對應問題 (1946)、詞語問題、Hilbert 第 10 問題 (1970)、Rice 定理（一切非平凡語義性質皆不可判定）。
- **通用電腦誕生**：通用圖靈機 = 軟硬體分離 = 馮諾依曼架構的理論源頭。Turing 戰後親自參與建造 ACE 與 Manchester 機。
- **計算複雜性理論**：1936 年問「能不能算」，1965 年後（Hartmanis–Stearns、Cobham）進一步問「算多快」——P vs NP 由此延伸。
- **Church–Turing 命題**成為計算的哲學基石：一切物理可實現的計算皆不超越圖靈機（量子計算也未推翻此命題，只改變了複雜度）。

## 關鍵人物與文獻
- **Alan Turing**（1912–1954）：On Computable Numbers, with an Application to the Entscheidungsproblem (1936, Proc. London Math. Soc.)；更正 (1937)
- **Alonzo Church**：An Unsolvable Problem of Elementary Number Theory (1936)——獨立解決判定問題
- **Emil Post**：獨立提出等價的計算模型 (1936)
- **John von Neumann**：EDVAC 報告 (1945)——通用圖靈機的工程實現
- 交叉參照：`1900-Hilbert23問題.md`、`1931-Godel不完備定理.md`、`1933-Lambda可定義性.md`
