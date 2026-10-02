# 1858 - Cayley《A Memoir on the Theory of Matrices》

## 案件摘要
1858 年，英國數學家 Arthur Cayley 發表《A Memoir on the Theory of Matrices》，首次將「矩陣」從行列式的附屬品提升為獨立的數學物件，定義矩陣加法、純量乘法與乘法，並證明 Cayley–Hamilton 定理。偵探的結論：這是一樁「從工具到主角」的身份翻轉案。

## 前因 -- 為什麼會有這個案子
- **行列式的長久統治**：自 17 世紀關島（Seki Takakazu）與 Leibniz 以降，行列式一直是處理聯立線性方程組的主要工具。19 世紀 Cauchy、Jacobi 將行列式理論系統化，但行列式只是一個「數」——一個附著於方形陣列的純量。
- **線性方程組與線性變換的需求**：考慮線性變換
  $$y = Ax, \qquad A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$$
  人們逐漸意識到，真正承載「變換本身」的是那個陣列 $A$，而不是 $\det A$。
- **Cayley 的線索來源**：Cayley 在研究線性變換的複合（先做 $A$ 再做 $B$）時發現：複合運算的規則需要一種新的「陣列代數」——行列式理論無法描述「變換相乘」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：矩陣的誕生——從行列式中解放
Cayley 宣稱：一個 $m \times n$ 矩陣本身就是一個數學物件，不必依附於行列式。注意行列式只對方陣有定義，而矩陣可以是任意形狀：
$$A = \begin{pmatrix} a_{11} & \cdots & a_{1n} \\ \vdots & & \vdots \\ a_{m1} & \cdots & a_{mn} \end{pmatrix} \in M_{m \times n}(F)$$
Cayley 定義：
- **加法**：$(A+B)_{ij} = a_{ij} + b_{ij}$（形狀相同時）
- **純量乘法**：$(\lambda A)_{ij} = \lambda \, a_{ij}$
- **矩陣乘法**：$(AB)_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$

### 線索二：乘法不可交換——$AB \neq BA$
矩陣乘法對應「變換的複合」，而複合的順序是有影響的。取
$$A = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$$
則
$$AB = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}, \qquad BA = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}, \qquad AB \neq BA$$
這是歷史上第一個真正普遍的**非交換代數結構**（四元數 1843 年雖更早，但矩陣的不可交換性出現在日常線性變換之中）。矩陣環 $M_n(F)$ 滿足：
- 結合律：$(AB)C = A(BC)$
- 分配律：$A(B+C) = AB + AC$
- 單位元素：單位矩陣 $I$，滿足 $AI = IA = A$

### 線索三：Cayley–Hamilton 定理——矩陣滿足自身的特徵多項式
對 $n \times n$ 矩陣 $A$，定義特徵多項式
$$p(\lambda) = \det(\lambda I - A) = \lambda^n + c_{n-1}\lambda^{n-1} + \cdots + c_1 \lambda + c_0$$
**Cayley–Hamilton 定理**：每一個方陣都滿足它自己的特徵多項式，即
$$p(A) = A^n + c_{n-1} A^{n-1} + \cdots + c_1 A + c_0 I = O$$
Cayley 在 1858 年論文中只對 $2\times 2$（敘述）與 $3\times 3$（部分驗證）給出證明；一般情形的嚴格證明要到 Frobenius（1878）。以 $2\times 2$ 為例，$p(\lambda) = \lambda^2 - (\operatorname{tr} A)\lambda + \det A$，故
$$A^2 - (\operatorname{tr} A) A + (\det A) I = O$$
**推理**：這條定理是「多項式能作用於矩陣」的關鍵示範——矩陣可以代入多項式，這預示了矩陣環與多項式環之間的賦值同態 $F[\lambda] \to M_n(F)$，也奠定了後來 Jordan 標準形與最小多項式理論的基礎。

### 線索四：矩陣作為線性變換
矩陣的真正身分是線性映射 $\varphi: F^n \to F^m$，$y = Ax$。矩陣乘法恰好對應複合：
$$A(Bx) = (AB)x$$
可逆矩陣對應雙射線性變換，逆矩陣 $A^{-1}$ 滿足 $A^{-1}A = AA^{-1} = I$。Cayley 時代尚未有完備的「線性空間」概念（要等 Peano 1888），但矩陣的運算規則已經是線性代數的胚胎。

### Python 驗證 Cayley–Hamilton 定理
```python
import numpy as np

def verify_cayley_hamilton(A, rtol=1e-10):
    A = np.asarray(A, dtype=complex)
    n = A.shape[0]
    # 特徵多項式係數：p(λ) = λ^n + c_{n-1} λ^{n-1} + ... + c_0
    coeffs = np.poly(A)          # 由高次到低次
    result = np.zeros_like(A)
    for i, c in enumerate(coeffs):
        result += c * np.linalg.matrix_power(A, n - i)
    return np.allclose(result, np.zeros_like(A), atol=rtol)

rng = np.random.default_rng(0)
for n in range(2, 8):
    A = rng.standard_normal((n, n))
    print(f"n={n}: Cayley-Hamilton 成立 = {verify_cayley_hamilton(A)}")
```

輸出顯示每一階隨機矩陣都滿足 $p(A)=O$——1858 年 Cayley 的猜想，在電腦上瞬間得到大規模數值佐證。

## 結案 -- 後果與影響
- **線性代數的誕生**：矩陣成為獨立研究對象，配合 Frobenius 的矩陣秩與 Jordan 標準形（1870s），線性代數正式成型。
- **非交換代數的先聲**：$AB \neq BA$ 為後來的非交換環論、算子代數（von Neumann, 1930s）鋪路。
- **物理學的工具**：Heisenberg 矩陣力學（1925）直接使用矩陣乘法的不可交換性，$[x, p] = i\hbar$ 正是 $AB - BA$。
- **Cayley–Hamilton 的延續生命**：最小多項式、特徵值演算法、控制理論（狀態轉移矩陣 $e^{At}$ 的計算）至今仍依賴它。
- **結案陳詞**：Cayley 把「陣列」從行列式的僕人提拔為主角，這樁身份翻轉案，是現代線性代數的第一頁。

## 關鍵人物與文獻
- **Arthur Cayley (1821–1895)**：英國代數學家，劍橋大學，律師出身，發表論文近千篇。
- Cayley, A. (1858). *A Memoir on the Theory of Matrices*. Phil. Trans. R. Soc. Lond. 148, 17–37.
- Frobenius, G. (1878). 完整證明 Cayley–Hamilton 定理並發展矩陣秩理論。
- 交叉參照：`1893-抽象群公理化.md`（矩陣群是抽象群的重要範例）、`1930-VanderWaerden近代代數.md`（矩陣環進入現代代數教科書）。
