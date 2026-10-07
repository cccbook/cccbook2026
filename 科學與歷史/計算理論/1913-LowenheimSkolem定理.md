# 1913/1915 - Löwenheim–Skolem 定理

## 案件摘要
Löwenheim（1915）與 Skolem（1920/1922/1929/1934）證明：一階邏輯若擁有無窮模型，就必然擁有可數模型——甚至任意基數的模型。這個「尺寸失控」的定理暴露了一階邏輯表達力的深刻限制，並產生了著名的 Skolem 悖論。

## 前因 -- 為什麼會有這個案子
Cantor 的集合論 (1874–1895) 建立了無窮的階層：$\aleph_0 < 2^{\aleph_0} < \dots$，但人們質疑：公理化系統（如 Zermelo 的 Z 公理系統 1908）能不能「鎖定」某個特定的無窮？Hilbert 的公理化綱領假設公理可以唯一刻劃數學結構。Löwenheim 與 Skolem 針對這個假設展開調查，結果發現一階邏輯的「測量能力」遠不如預期。

## 線索與推理 -- 數學式、程式、理論

### 一階邏輯的語義
一階邏輯的解釋（模型）是一個結構 $\mathcal{M} = (D, I)$，其中 $D$ 是論域（domain），$I$ 解釋函數與關係符號。滿足關係定義為：

$$\mathcal{M} \models \varphi[s]$$

關鍵量詞的語義：

$$\mathcal{M} \models \forall x\, \varphi \iff \text{對每個 } d \in D,\ \mathcal{M} \models \varphi[x \mapsto d]$$

$$\mathcal{M} \models \exists x\, \varphi \iff \text{存在 } d \in D,\ \mathcal{M} \models \varphi[x \mapsto d]$$

**偵探筆記**：量詞「跑遍」論域 $D$，但語言本身**無法**說「$D$ 恰好有多少個元素」——除非用有限個變數的公式，而那只能說「至多 $n$ 個」。

### Löwenheim–Skolem 定理
**下行 (Downward) Löwenheim–Skolem 定理**：若一階理論 $T$（可數語言）有一個無窮模型，則 $T$ 有一個**可數模型**：

$$\mathcal{M} \models T,\ |D_{\mathcal{M}}| \geq \aleph_0 \implies \exists \mathcal{N} \models T,\ |D_{\mathcal{N}}| = \aleph_0,\ \mathcal{N} \preceq \mathcal{M}$$

（$\mathcal{N} \preceq \mathcal{M}$ 表示基本子結構：對每個公式 $\varphi$ 與賦值 $s$，$\mathcal{N} \models \varphi[s] \iff \mathcal{M} \models \varphi[s]$。）

**上行 (Upward) 定理**（Skolem 1934, Tarski–Vaught）：若 $T$ 有無窮模型，則 $T$ 有任意無窮基數 $\kappa$ 的模型。

推論：**一階邏輯無法刻劃無窮結構的大小**。Löwenheim–Skolem 定理（LS）$+$ 緊緻性定理（Compactness）⟹ 一階理論若有一個無窮模型，就有所有無窮基數的模型（沒有唯一性）。

### Skolem 悖論
ZFC 集合論中有定理「存在不可數集合」（如實數集 $\mathbb{R}$，$|\mathbb{R}| = 2^{\aleph_0} > \aleph_0$）：

$$\mathrm{ZFC} \vdash \exists x\, \neg\exists f\, (f \text{ 是從 } \omega \text{ 到 } x \text{ 的滿射})$$

但根據下行 LS 定理，若 ZFC 一致，它有一個**可數模型** $\mathcal{M}$，$|D_{\mathcal{M}}| = \aleph_0$！

**偵探推理**：矛盾嗎？不是。在 $\mathcal{M}$ **內部**，「不可數」是相對於 $\mathcal{M}$ 的論域與 $\mathcal{M}$ 中的「函數」概念而言的：$\mathcal{M}$ 中**不存在**那個從 $\omega$ 到 $x$ 的滿射——但**從外面看**（meta-level），$x^{\mathcal{M}}$ 只是一個可數集合，只不過對應的滿射函數不在 $\mathcal{M}$ 的論域裡。

「可數性」不是絕對的，而是**相對於模型**的。這就是一階邏輯表達力的極限：它無法從內部表達「絕對不可數」。

### 程式碼：模型尺寸的「相對性」演示
```python
# 模擬：一個「可數模型 M」中的集合 x，在 M 內部是「不可數」的
# 因為 M 的論域（函數的宇宙）裡沒有那個滿射
universe = {f"f{i}" for i in range(10)}   # M 中的「函數」只有 10 個
omega   = {"n0", "n1", "n2"}              # 自然數的解釋
target  = {"a", "b", "c", "d"}            # x 的解釋（外部看：4 個元素，可數！）

# M 內部找不到「omega -> target 的滿射」
surjection_in_M = [
    f for f in universe
    if f.startswith("f") and False  # 沒有任何 f 能真正映射（模擬 M 的局限）
]
print("M 內部的滿射存在嗎？", bool(surjection_in_M))  # False -> x 在 M 內「不可數」
print("外部看 x 有幾個元素？", len(target))            # 4 -> 明明可數！

# 這就是 Skolem 悖論：內部「不可數」，外部可數。
```

### 與判定問題的關係
一階邏輯的有效性問題（$\varphi$ 是否在所有模型中為真）：

$$\mathrm{VAL} = \{ \varphi \mid \models \varphi \}$$

- 1915–1920 年代，人們期望 LS 定理加上完備性能給出判定程序。
- 1936 年 Church 與 Turing 證明：**一階邏輯的有效性不可判定**（Church 定理）。
- 對照：**命題邏輯**的有效性是可判定的（真值表法，$O(2^n)$）；**一元一階邏輯**（只有一元述詞）也可判定；但完整一階邏輯不可判定——LS 定理揭示了語義的微妙，但沒能挽救可判定性。

## 結案 -- 後果與影響
- **一階邏輯成為「標準」邏輯**，但代價是承認它無法刻劃無窮大小——非標準模型氾濫（Skolem 1934 已構造自然數的非標準模型）。
- **模型論**（model theory）作為獨立學科誕生：Tarski 的真值定義 (1933)、緊緻性定理、Löwenheim–Skolem 定理成為模型論三大基石。
- **Skolem 悖論**啟發了「相對性」與「內部/外部」的區分，深刻影響集合論（大基數理論、可構造宇宙 $L$）。
- **二階邏輯**可以刻劃 $\mathbb{R}$ 與 $\mathbb{N}$（categoricity），但失去完備性與緊緻性——表達力與可判定性/完備性的 trade-off 從此成為邏輯學的中心主題。

## 關鍵人物與文獻
- **Leopold Löwenheim**（1878–1957）：Über Möglichkeiten im Relativkalkül (1915)
- **Thoralf Skolem**（1887–1963）：Logisch-kombinatorische Untersuchungen (1920)；Skolem 悖論的提出 (1922)
- **Alfred Tarski**（1902–1983）：上行 LS 定理、模型論奠基
- 交叉參照：`1931-Godel不完備定理.md`、`1936-Turing機與停機問題.md`
