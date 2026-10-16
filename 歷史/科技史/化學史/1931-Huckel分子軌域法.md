# 1931 Hückel 分子軌域法

## 案發現場

1930 年前後，化學理論正處於一場深刻的轉型：量子力學在 1925–1927 年間誕生（Heisenberg、Schrödinger、Dirac），Pauling 把量子力學帶進化學，發展了價鍵理論（valence bond theory）。但有機化學最大的謎題——**苯的結構與芳香性**——仍然沒有令人滿意的答案。

苯（$\mathrm{C_6H_6}$）自 1825 年由 Faraday 發現以來，困擾化學家一百年：1865 年 Kekulé 提出了六角環結構，用「交替單鍵雙鍵」與「振盪假說」解釋苯的性質。但這個結構有明顯的缺陷：如果苯真的是三個雙鍵交替的環，它應該像環己三烯一樣容易進行加成反應，但苯卻異常地**不活潑**——它偏好取代反應而抗拒加成；它的六個 C–C 鍵長完全相等（1.397 Å，介於單鍵 1.54 Å 與雙鍵 1.34 Å 之間）；它比「理論值」更穩定，氫化熱比預期少了約 150 kJ/mol（這個差值被稱為「共振能」或「芳香性穩定化能」）。

1928–1931 年，德國斯圖加特理工學院、後任教於萊比錫的物理化學家埃里希·休克爾（Erich Hückel）正在研究一個基礎問題：如何用量子力學處理**不飽和有機分子**。他的妻子是位有機化學家，家常對話中苯的謎題不斷提醒他這個問題的重要性。當時的有機化學家覺得量子力學太抽象、太數學化，跟試管裡的化學無關——休克爾要證明的恰恰相反：**量子力學可以解開苯的謎題，並預測哪些分子有「芳香性」**。

## 偵查過程

休克爾的偵查分三步，每一步都建立了理論化學的方法論。

第一步是**簡化**。休克爾注意到苯的電子結構可以分成兩類：$\sigma$ 電子（C–C、C–H 鍵上的電子，分布在分子平面內，較定域）與 $\pi$ 電子（p 軌域上的電子，垂直於分子平面，可以離域到整個環）。他提出一個大膽的簡化：**先忽略 $\sigma$ 電子（把它們視為固定的骨架），只處理 $\pi$ 電子**。這就是「休克爾近似」的核心，它把一個 42 電子的問題（苯）簡化成 6 電子的問題，使得手算成為可能。

第二步是 **LCAO（原子軌域線性組合）**。休克爾假設每個 $\pi$ 分子軌域（MO）是六個碳的 p 軌域的線性組合：

$$\psi_k = \sum_{i=1}^{6} c_{ki}\,\phi_i$$

其中 $\phi_i$ 是第 $i$ 個碳的 $2p_z$ 軌域，$c_{ki}$ 是組合係數。把這個形式代入變分原理 $\frac{\partial}{\partial c_{ki}}\langle\psi|\hat{H}|\psi\rangle = 0$，就得到一組線性方程組，其非平凡解存在的條件是「久期行列式」（secular determinant）為零：

$$\begin{vmatrix}
\alpha - E & \beta & 0 & 0 & 0 & \beta \\
\beta & \alpha - E & \beta & 0 & 0 & 0 \\
0 & \beta & \alpha - E & \beta & 0 & 0 \\
0 & 0 & \beta & \alpha - E & \beta & 0 \\
0 & 0 & 0 & \beta & \alpha - E & \beta \\
\beta & 0 & 0 & 0 & \beta & \alpha - E
\end{vmatrix} = 0$$

第三步是**參數化**。休克爾做了兩個關鍵的參數假設：
- **庫倫積分** $\alpha = \langle\phi_i|\hat{H}|\phi_i\rangle$：所有碳都相同，故對角元都是 $\alpha$（約等於 p 電子的能量）。
- **共振積分** $\beta = \langle\phi_i|\hat{H}|\phi_j\rangle$（相鄰原子）：所有相鄰的 C–C 都相同；不相鄰的則設為零（忽略）。

這兩個參數不必真的算出來，而是從實驗數據（如氫化熱）反推——**理論的結構是嚴格的，參數是經驗的**，這就是「半經驗方法」的誕生。

解苯的久期方程（利用分子對稱性或直接求解），得到六個 $\pi$ 軌域能量：

$$E = \alpha + 2\beta,\quad \alpha + \beta,\ \alpha + \beta,\quad \alpha - \beta,\ \alpha - \beta,\quad \alpha - 2\beta$$

（$\beta$ 為負值，能量越低越穩定。）苯的 6 個 $\pi$ 電子按照構造原理填入：2 個填入最低軌域 $\alpha + 2\beta$，4 個填入兩個簡併軌域 $\alpha + \beta$。總 $\pi$ 電子能量為：

$$E_\pi = 2(\alpha + 2\beta) + 4(\alpha + \beta) = 6\alpha + 8\beta$$

如果苯是「三個孤立雙鍵的環己三烯」，其能量為 $3 \times (2\alpha + 2\beta) = 6\alpha + 6\beta$。兩者的差值就是**芳香性穩定化能**：

$$\Delta E_{\text{芳香}} = (6\alpha + 8\beta) - (6\alpha + 6\beta) = 2\beta \approx -150\ \mathrm{kJ/mol}$$

（以 $\beta \approx -75\ \mathrm{kJ/mol}$ 標定。）這正是苯氫化熱「少了 150 kJ/mol」的量子力學解釋！苯之所以不活潑，是因為它的 $\pi$ 電子離域在整個環上，形成了一個能量特別低的「電子海洋」。

休克爾更進一步，把同樣的方法應用到其他環狀共軛分子，發現一個優雅的規律：**平面單環共軛分子若具有 $4n+2$ 個 $\pi$ 電子（$n = 0, 1, 2, \ldots$），就具有芳香性**。這就是「休克爾芳香性規則」：

$$\pi\text{ 電子數} = 4n + 2 \Rightarrow \text{芳香性（穩定）}$$

- 苯（6 電子，$n=1$）：芳香 ✓
- 環丁二烯（4 電子）：反芳香（antiaromatic，特別不穩定，實際上極難存在）✗
- 環戊二烯陰離子（6 電子）：芳香 ✓
- 環辛四烯（8 電子）：非平面（避開反芳香）或反芳香 ✗
- 輪烯類（如 [18]annulene，18 電子，$n=4$）：芳香 ✓

規則的量子力學根源：對 $N$ 個碳的單環，$\pi$ 軌域能量為 $E_k = \alpha + 2\beta\cos(2\pi k/N)$。當 $N$ 為偶數且 $\pi$ 電子數為 $4n$ 時，會出現**半填滿的簡併軌域**（開殼層、能量不利的 Jahn-Teller 畸變）；而 $4n+2$ 個電子剛好填滿所有成鍵軌域，形成**閉殼層的穩定結構**。休克爾規則因此不是經驗巧合，而是量子力學的直接推論。

## 結案報告

1931 年，休克爾發表了三篇系列論文《Quanstentheorie der aromatischen Verbindungen》（芳香化合物的量子理論），建立了 Hückel 分子軌域法（HMO）。遺產包括：

1. **芳香性有了定量定義**：休克爾規則成為有機化學的核心判據，指導了一百年的合成設計——從環戊二烯陰離子、雜環（吡啶、呋喃、噻吩）到富勒烯、石墨烯，芳香性概念不斷擴展。當今的「雙芳香性」「Möbius 芳香性」等概念都是休克爾規則的延伸。
2. **理論化學進入有機化學**：休克爾證明量子力學可以解決有機化學的實際問題（苯的穩定性、環丁二烯的不存在、輪烯的性質），理論化學從此成為有機化學的標準工具。1950 年代，休克爾的學生與後繼者（如 Pople、Dewar）發展出更精確的半經驗方法（CNDO、MNDO 等），最終演化為今天的 DFT 計算化學。
3. **HMO 方法論的範式**：「LCAO + 久期方程 + 經驗參數」的三步法，成為理論化學的標準工作流程。HMO 至今仍是大學化學系量子化學課程的入門方法——它簡單到可以手算，卻能給出定量的預測。
4. **分子軌域理論的勝利**：休克爾的工作（連同 Mulliken 的 MO 理論）證明 MO 方法比價鍵理論更能解釋離域現象，最終 MO 成為化學鍵理論的主流。1966 年 Mulliken 獲得諾貝爾化學獎。
5. **與實驗的對話**：休克爾規則預測環丁二烯特別不穩定、[18]annulene 芳香——這些預測在 1950–1960 年代被一一實驗驗證，理論與實驗的互動成為化學史的典範。

一百年苯的謎題，被一位物理化學家用「忽略 $\sigma$ 電子」的簡化思想解開。休克爾的方法證明：**化學的直覺（芳香性、穩定性）背後是數學的結構（久期行列式、特徵值）**——這是理論化學第一次真正「接管」有機化學。

## 證據與工具

以下用 Python（numpy 特徵值）實際解出苯與其他單環分子的 Hückel 矩陣，驗證 $4n+2$ 芳香性規則。

```python
import numpy as np
import matplotlib.pyplot as plt

# --- 休克爾參數 ---
alpha = 0.0     # 庫倫積分(設為能量原點)
beta  = -1.0    # 共振積分(能量單位, 負值 = 成鍵)

# --- 建構 Hückel 矩陣 ---
def huckel_matrix(n, closed=True):
    """單環 n 個碳的 Hückel 矩陣: 相鄰 = beta, 其餘 = 0"""
    H = np.zeros((n, n))
    for i in range(n):
        H[i, (i+1) % n] = beta          # 右鄰(環狀: 末尾接回首)
        H[i, (i-1) % n] = beta          # 左鄰
    return H

# --- 解苯 (C6H6, 6 個 pi 電子) ---
H_benzene = huckel_matrix(6)
energies, coeffs = np.linalg.eigh(H_benzene)
print("苯的 Hückel pi 軌域能量 (單位 beta):")
for i, e in enumerate(energies):
    print(f"  MO {i+1}: E = {e:.3f}  (填充電子: {2 if i < 3 else 0})")

E_pi = 2 * sum(energies[:3])            # 6 個電子填入最低 3 個軌域
E_ref = 3 * (2*alpha + 2*beta)          # 環己三烯: 3 個孤立雙鍵
print(f"\n苯 E_pi = {E_pi:.2f} β, 環己三烯 = {E_ref:.2f} β")
print(f"芳香性穩定化能 = {E_pi - E_ref:.2f} β ≈ 2β (~150 kJ/mol)")
print("→ 苯比「三個雙鍵」更穩定，這就是不活潑的量子力學解釋\n")

# --- 驗證 4n+2 芳香性規則 ---
print("休克爾芳香性規則驗證 (4n+2):")
print(f"{'環大小':>6} {'pi電子':>6} {'4n+2?':>6} {'穩定化能':>10} {'判斷':>8}")
for n in range(4, 11):
    H = huckel_matrix(n)
    e, _ = np.linalg.eigh(H)
    n_e = n                             # 每個碳 1 個 pi 電子
    n_occ = n_e // 2
    E_pi_n = 2 * sum(e[:n_occ]) + (n_e % 2) * e[n_occ]
    E_open = n_e * (alpha + beta)       # n 個孤立雙鍵的參考
    stab = E_pi_n - E_open
    aromatic = "✓ 芳香" if stab < -1.5 else ("✗ 反芳香" if stab > 0 else "△ 非芳香")
    print(f"{n:>6} {n_e:>6} {'是' if n_e % 4 == 2 else '否':>6} "
          f"{stab:>10.2f} {aromatic:>8}")

# --- 視覺化: pi 軌域能級圖 ---
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, n, title in zip(axes, [6, 4, 8], ['苯(6e) 芳香', '環丁二烯(4e) 反芳香', '環辛四烯(8e) 反芳香']):
    H = huckel_matrix(n)
    e, _ = np.linalg.eigh(H)
    n_occ = n // 2
    for i, energy in enumerate(e):
        color = '#4C9BE8' if i < n_occ else '#E8674C'
        occ_e = 2 if i < n_occ else 0
        for _ in range(occ_e):
            ax.plot([0, 1], [energy, energy], color=color, lw=4)
        ax.plot([0, 1], [energy, energy], 'k-', lw=0.5)
    ax.axhline(0, color='gray', ls='--')
    ax.set_title(title); ax.set_ylabel('能量 (β)'); ax.set_xticks([])
plt.suptitle('休克爾 pi 軌域能級圖: 4n+2 電子填滿成鍵軌域 → 閉殼層穩定')
plt.show()
```
