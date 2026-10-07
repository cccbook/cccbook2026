# 1984 — de Branges 證明 Bieberbach 猜想

## 案件摘要
1916 年，Bieberbach 提出一個看似小學生都懂的猜想：單葉函數 $f(z) = z + a_2z^2 + a_3z^3 + \cdots$ 的係數必滿足 $|a_n| \le n$。這個案子整整懸宕 **68 年**，途中動用面積定理、Loewner 參數法、無數數學家的青春，甚至因錯誤的「證明」毀掉職業生涯。1984 年，Purdue 的 Louis de Branges 用 Hilbert 空間的算子理論一舉結案：$|a_n| \le n$ 對所有 $n$ 成立，等號僅在 Koebe 函數 $z/(1-z)^2$ 上出現。

## 前因 -- 為什麼會有這個案子
- 1907 年 Koebe 找到極值函數 $f(z) = z/(1-z)^2 = z + 2z^2 + 3z^3 + \cdots$：它把單位圓盤共形映射到整個平面去掉負實軸上的射線。所有係數都是 $n$——猜想的天花板就此現形。
- 1916 年 Bieberbach 只證到 $|a_2| \le 2$，卻大膽猜想 $|a_n| \le n$ 對所有 $n$ 成立。手段與目標之間的巨大落差，正是此案纏訟 68 年的原因。
- 1923 年 Loewner 用「參數法」證出 $|a_3| \le 3$——之後每前進一個係數都要數年甚至數十年。
- 錯案插曲：68 年間多篇「證明」被發現有漏洞而撤回，受害者包括知名數學家的聲譽；FitzGerald 在 1972 年只把一般係數界推進到 $|a_n| \le \sqrt{7/6}\,n \approx 1.08\,n$——離天花板一步之遙卻始終跨不過去。這是數學史上最著名的「懸案」之一。

## 線索與推理 -- 數學式、程式、理論

### 線索一：單葉函數與係數問題
設 $\mathcal{S}$ 為單位圓盤上的正規化單葉（一對一共形）解析函數族：

$$f(z) = z + \sum_{n=2}^{\infty} a_n z^n, \qquad |z| < 1$$

單葉性是強約束：$f$ 不能折疊。直覺上「不折疊」應該限制係數大小——Bieberbach 猜想斷言：

$$|a_n| \le n, \quad n = 2, 3, 4, \dots$$

等號當且僅當 $f$ 是 Koebe 函數 $z/(1-z)^2$ 的旋轉。注意 Koebe 函數的係數恰為 $1, 2, 3, 4, \dots$，正是一條直線——它就是「最極端」的單葉函數。

### 線索二：面積定理（Gronwall, 1914）
考慮 $\mathcal{S}$ 中函數的補集映射 $g(w) = w - b_1/w - b_2/w^2 - \cdots$，把單位圓外映射到像集補集。Gronwall 的**面積定理**說：

$$\sum_{n=1}^{\infty} (2n-1)\,|b_n|^2 \le 1$$

特別地 $|b_1| \le 1$。面積定理是第一件真正的兇器：它證明了像補集的面積不超過圓盤面積，從而壓住係數。但它只對補集係數有效，對 $a_n$ 只能推出 $|a_n|$ 的次線性上界，不足以證明 $|a_n| \le n$。

### 線索三：Loewner 參數法與 de Branges 的 Hilbert 空間證明
Loewner（1923）發現：任何 $\mathcal{S}$ 中的單葉函數都可以由一族「增長過程」$f_t(z) = e^t z + \cdots$（$0 \le t < \infty$）生成，滿足偏微分方程：

$$\frac{\partial f_t}{\partial t} = \frac{\partial f_t}{\partial z}\, \varphi_t(f_t(z)) \cdot \frac{1}{\varphi_t} $$

其中 $\varphi_t$ 是模長 1 的函數。這把靜態的係數問題變成動態的演化問題。1984 年 de Branges 的關鍵一步：證明 Hilbert 空間上一族壓縮算子的「冪級數展開」滿足某組不等式，再藉由一個細膩的引理（de Branges 引理，關於實對稱核的矩陣不等式）推出：若 $f \in \mathcal{S}$ 則對每個 $n$，

$$\sum_{k=1}^{n} k\,|a_k|^2 \cdot \phi(n, k) \le \dots \quad \Rightarrow \quad |a_n| \le n$$

證明發表後，Leningrad 的數學家們（Milin、Khrushchev 等）用Loewner 理論的 Milin 猜想獨立驗證了核心步驟，FitzGerald 與 Pommerenke 也給出簡化證明。懸案正式告破。

### 線索四：數值檢驗——已知最好係數界與 Koebe 函數
在 de Branges 之前，已知的最好結果是：$|a_2|\le 2$（Bieberbach 1916）、$|a_3|\le 3$（Loewner 1923）、$|a_4|\le 4$（1936）、直到 $|a_6|\le 6$（1968）——每個都恰好貼著天花板。數值上，係數界從未「超過」$n$。

### 程式碼範例：Bieberbach 係數 $|a_n| \le n$ 的級數檢驗
```python
import numpy as np

# Koebe 函數 f(z) = z/(1-z)^2 的 Taylor 係數應為 a_n = n
N = 20
# 直接用級數 1/(1-z)^2 = sum (n+1) z^n 乘 z
n = np.arange(1, N + 1)
a_koebe = n.astype(float)
print("Koebe 係數 a_n:", a_koebe[:10])
print("檢驗 |a_n| <= n:", np.all(np.abs(a_koebe) <= n))

# 數值驗證：對旋轉 Koebe 函數 e^{iθ} f(e^{-iθ} z)，
# 係數模長不變，仍為 n —— 極值族的封閉性
theta = np.pi / 5
f = lambda z: np.exp(1j*theta) * z / (1 - np.exp(-1j*theta)*z)**2
r = 0.99
zk = r * np.exp(1j * np.linspace(0, 2*np.pi, 4096, endpoint=False))
w = f(zk)
# 用 FFT 從圓周取樣反推係數（Cauchy 積分的數值版）
coeffs = np.fft.fft(w) / len(w)   # 第 k 項 ≈ a_k r^k
a_num = np.abs(np.fft.fftshift(coeffs)[len(w)//2 + 1: len(w)//2 + 1 + N]) / r**n
print("FFT 反推係數 (前5):", np.round(a_num[:5], 4), "理論:", n[:5])

# 對照：非極值函數 f(z) = z/(1-z) 的係數全為 1
a2 = np.ones(N)
print("z/(1-z) 係數模長全為 1，遠低於天花板 n")
```

FFT（即 Cauchy 積分公式 $\frac{1}{2\pi i}\oint \frac{f(z)}{z^{k+1}}dz$ 的離散版本）從圓周取樣精確反推出 Koebe 函數的係數 $a_n = n$——天花板函數在數值上一覽無遺，$|a_n| \le n$ 從未被違反。

## 結案 -- 後果與影響
- **單葉函數論結案**：68 年懸案終結，$\mathcal{S}$ 族的係數問題、成長問題、覆蓋問題全部有了解答框架。
- de Branges 的證明開啟**函數空間方法**：Hilbert 空間算子、核函數理論從此成為幾何函數論的標準工具。
- **計算機輔助**的角色被正視：de Branges 的證明發表前，蘇聯學者用計算機驗證了 Milin 不等式的前幾十個案例，增強了數學界的信心——這是數學證明中計算驗證的早期範例。
- de Branges 因此案獲 1994 年 Ostrowski 獎；他後續的 Hilbert 空間理論（de Branges 空間）成為整函數論與 Riemann zeta 相關研究的工具。
- 教科書改寫：Duren《Univalent Functions》、Pommerenke《Boundary Behaviour》把結案過程完整記錄。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Louis de Branges | 1984 年證明猜想 |
| Ludwig Bieberbach | 1916 年提出猜想 |
| Paul Koebe | 1907 年找到極值函數 $z/(1-z)^2$ |
| Karl Löwner (Loewner) | 1923 年參數法，證 $|a_3| \le 3$ |
| James Gronwall | 1914 年面積定理 |

- L. de Branges, *A proof of the Bieberbach conjecture*, Acta Math. **154**, 137–170 (1985)。
- L. Bieberbach, Math. Ann. **77**, 153 (1916)。
- P. L. Duren, *Univalent Functions*, Springer (1983)。
- C. Pommerenke, *Univalent Functions*, Vandenhoeck (1975)。
