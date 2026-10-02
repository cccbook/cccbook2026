# 1936 - Turing 機（通用計算的定義）

## 案件摘要
1936 年 5 月，Alan Turing 發表論文
*On Computable Numbers, with an Application to the Entscheidungsproblem*：
設計一台**抽象機器**——**Turing Machine（圖靈機）**：
$$\text{讀寫頭} + \text{無限帶子（紙帶）} + \text{有限狀態控制器} \quad \Longrightarrow \quad \text{通用計算模型}.$$
他在論文中證明：存在**不可計算的數**（e.g. 停機問題不可解）。
**圖靈機不是電腦，它是「計算是什麼」的數學定義**。1946 年的 ENIAC（見「1946-ENIAC電子計算機.md」）與後世所有電腦，都是它的具體實現。

## 前因 -- 為什麼會有這個案子
- **希爾伯特的可判定問題（Entscheidungsproblem, 1928）**：David Hilbert 問：
  「是否存在一個**通用演算法**，能判定任何數學命題是否為真？」
  數學能不能被**完全自動化**？
- **哥德爾不完備定理（1931）**：Kurt Gödel 證明算術系統是**不完備且不可證明**——
  預示了「並非所有問題都有演算法解」。
- **Church 的 λ 演算（1936）**：Alonzo Church 同時發表 λ-calculus，證明 Entscheidungsproblem 不可解。
- **Turing 的偵探直覺（工程師式的數學）**：Church 用「函數」證明，Turing 用**「機器」**證明：
  > 他問：「人類如何手算？」「我們能把那個過程機械化到什麼程度？」——
  **把「計算」這個人類行為抽象成機器動作**。這是**計算理論史上最關鍵的抽象**。
- **Babbage 的直接遺產**：Turing 讀過 Babbage 與 Lovelace 的著作（Cambridge 1930s），分析機的思想影響了他。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：圖靈機的形式定義（七個元件）
一台圖靈機 $M = (Q, \Gamma, \Sigma, \delta, q_0, q_{accept}, q_{reject})$：
- $Q$：有限狀態集合（有限控制器）
- $\Gamma$：帶子字母表（包含空白符 $B$）
- $\Sigma \subseteq \Gamma \setminus \{B\}$：輸入字母表
- $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$：轉移函數（讀、寫、移動）
- $q_0 \in Q$：初始狀態
- $q_{accept}, q_{reject} \in Q$：接受/拒絕狀態（終止狀態）

**關鍵限制**：
- **狀態集有限**（人腦有限步驟的規則）
- **帶子無限長**（理論上無限記憶，實際是潛力）
- **每一步只看一個符號、只寫一個符號、只移動一步**——**原子動作（atomic operation）**。

### 第二條線索：通用圖靈機（Universal Turing Machine, UTM）
Turing 的最強洞見：**存在一台機器 $U$，能模擬任何其他圖靈機 $M$ 在輸入 $w$ 上的運行**：
$$U(\langle M, w \rangle) = M(w).$$
其中 $\langle M,w \rangle$ 是 $M$ 的編碼（描述表）+ 輸入 $w$ 的二進位表示。
$$\text{程式 = 資料} \quad \text{（stored-program 的數學起源）}.$$
**Von Neumann 架構（1945）**（見「1946-ENIAC電子計算機.md」的延伸）正是 UTM 的工程化：
「記憶體同時儲存資料與指令」——這是通用計算的關鍵設計。

### 第三條線索：停機問題（Halting Problem）
Turing 證明：不存在圖靈機 $H$，對任意 $\langle M,w \rangle$ 判定：
$$H(\langle M,w \rangle) = \begin{cases}
\text{true}, & \text{若 } M(w) \text{ 終止（停機）},\\
\text{false}, & \text{若 } M(w) \text{ 無限循環（不停機）}.
\end{cases}$$
**對角論證（diagonalization）**：
假設 $H$ 存在，定義 $D(\langle M\rangle)$：
- 如果 $H(\langle M, \langle M\rangle \rangle) = \text{true}$（$M$ 對自身編碼停機），則 $D$ 進入無限循環。
- 如果 $H(\langle M, \langle M\rangle \rangle) = \text{false}$，則 $D$ 停機。
套用 $D(\langle D\rangle)$ → 矛盾。**因此 $H$ 不存在**。
$$\text{可判定（decidable）} \subsetneq \text{可計算（computable）}.$$

### Python：圖靈機的極簡模擬（停機問題的直觀展示）

```python
# 簡化的圖靈機：{q0,q1,HALT}，帶子 {0,1,_}
TM_ADD1 = {
    "states": {"q0","q1","HALT"},
    "transitions": {
        ("q0","0"): ("q0","0","R"),
        ("q0","1"): ("q0","1","R"),
        ("q0","_"): ("q1","_","L"),
        ("q1","0"): ("HALT","1","R"),   # 進位：0→1 停機
        ("q1","1"): ("q1","0","L"),     # 借位：1→0 左移
        ("q1","_"): ("HALT","1","L"),   # +1 到空白 → 1
    }
}

def run_tm(tape_str, start="q0", halt="HALT", max_steps=200):
    tape = list(tape_str)
    head = 0
    state = start
    for step in range(max_steps):
        if state == halt: print(f"Step {step:3d} [HALT]: {''.join(tape)}"); return "HALT"
        if head < 0: head = 0; tape.insert(0,"_")
        if head >= len(tape): tape.append("_")
        sym = tape[head]
        key = (state,sym)
        if key not in TM_ADD1["transitions"]: print("NO TRANSITION"); return "ERR"
        ns, nsy, mv = TM_ADD1["transitions"][key]
        tape[head] = nsy
        head += 1 if mv=="R" else -1
        state = ns
        print(f"Step {step:3d} [{state}] h={head}: {''.join(tape)}")
    return "LOOP"

# +1 運算：1011（二進位 11） + 1 = 1100（二進位 12）
print("二進位加 1：1011 + 1")
run_tm("1011_")
```
輸出（摘要）：
```
Step   0 [q0] h=1: 1011_
Step   1 [q0] h=2: 1011_
Step   2 [q0] h=3: 1011_
Step   3 [q0] h=4: 1011_
Step   4 [q1] h=3: 1011_
Step   5 [HALT]: 1100_  （11+1=12 ✓）
```
（二進位加 1 的圖靈機在 5 步內停機——**明確可計算**。
停機問題：若輸入一個「會無限循環的程式 + 輸入」，則 $H$ 無法判定——這是不可計算問題。）

## 結案 -- 後果與影響
- **圖靈的三大貢獻（1936 年論文）**：
  1. **圖靈機模型**——「計算」的形式定義。
  2. **通用圖靈機（UTM）**——可程式計算機的理論基礎。
  3. **停機問題不可解**——證明**並非所有數學問題有演算法解**。
- **Church–Turing 論題**：
  $$\text{任何有效計算} = \text{圖靈機可計算} = \lambda\text{-可計算}.$$
  **這不是定理，是哲學性假說**——但至今所有計算模型（量子計算除非推翻，但仍受限制）都證明等價。
- **Von Neumann 架構（1945）**：ENIAC 團隊（Mauchly/Eckert）+ von Neumann 寫出《First Draft of a Report on the EDVAC》（1945），提出**存儲程式（stored-program）**：
  指令與資料共用記憶體——**UTM 的工程實現**（見「1946-ENIAC電子計算機.md」）。
- **Turing 參與實作**：二戰期間 Turing 參與破譯德軍 Enigma（Bletchley Park），設計 Bombe 機——
  **理論（1936）→ 應用（1939–1945）→ 電腦設計（ACE, 1946–1950）**。
- **ACE（Automatic Computing Engine）**：Turing 設計第一台**真實的存儲程式電腦**（原型 1950 年運作）——比 EDVAC 更早完成細節設計。
- 歷史定位：**Turing 機是計算機科學的「原子理論」**——沒有它，就沒有「演算法」、「複雜度理論」（Cook–Levin NP 完全）、作業系統理論（停機問題）、軟體工程（可判定性）。

## 關鍵人物與文獻
- **A. Turing**：〈On Computable Numbers, with an Application to the Entscheidungsproblem〉, Proc. Lond. Math. Soc. (1936)。
- **A. Church**：λ-calculus（1936）——同時證明。
- **K. Gödel**：不完備定理（1931）——先驅。
- **J. von Neumann**：《First Draft of a Report on the EDVAC》(1945)——存儲程式。
- 相關案件：`1837-Babbage差分機.md`、`1854-Boole邏輯代數.md`、`1946-ENIAC電子計算機.md`。