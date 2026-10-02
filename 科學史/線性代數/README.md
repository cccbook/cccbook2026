# 線性代數史 -- AI 偵探風格

以「推理探案」的方式，追查線性代數從《九章算術》的損益消去法，到今日 GPU 與 Transformer 的矩陣乘法，每一步的前因是什麼？線索在哪裡？推理如何展開？後果又如何重塑了整個數學、物理與資訊科學？

這樁「懸案」橫跨兩千三百年：中國算籌早就會解聯立方程，Leibniz 與 Cramer 替它取了「行列式」的名字，Grassmann 看見了 n 維空間卻無人理會，Cayley 給了它「矩陣」的語言，Peano 寫下公理、Markov 讓它動起來，Strassen 打破 $O(n^3)$——而今天，矩陣乘法就是每一個大型語言模型的心臟。

## 案件卷宗（歷史年表）

### 遠古與行列式前夜（前 300–1795）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 前300 | 《九章算術》方程章：聯立方程組的「損益」消去法，Gaussian elimination 遠古原型 | [前300-九章算術聯立方程.md](前300-九章算術聯立方程.md) |
| 1637 | Descartes《幾何學》：座標系把幾何轉成代數，線性變換的搖籃 | [1637-Descartes座標幾何.md](1637-Descartes座標幾何.md) |
| 1693 | Leibniz 首次寫下行列式 $a_1b_2-a_2b_1$ | [1693-Leibniz行列式.md](1693-Leibniz行列式.md) |
| 1750 | Cramer 法則 $x_i=\det(A_i)/\det(A)$，以行列式解聯立方程 | [1750-Cramer法則.md](1750-Cramer法則.md) |
| 1772 | Vandermonde 首度把行列式當獨立研究對象 $\prod_{i<j}(x_j-x_i)$ | [1772-Vandermonde行列式.md](1772-Vandermonde行列式.md) |
| 1795 | Gauss 最小平方法 $A^TA\hat{x}=A^Tb$，以 Ceres 軌道預測成名 | [1795-Gauss最小平方法.md](1795-Gauss最小平方法.md) |
| 1787 | Lagrange 二次型化簡（配方→平方和），特徵值理論前奏 | [1787-Lagrange二次型化簡.md](1787-Lagrange二次型化簡.md) |

### 行列式時代（1812–1850）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1812 | Cauchy 行列式理論：$\det(AB)=\det(A)\det(B)$ | [1812-Cauchy行列式理論.md](1812-Cauchy行列式理論.md) |
| 1827 | Möbius 重心座標與仿射變換，Grassmann 的直接前驅 | [1827-Möbius重心座標.md](1827-Möbius重心座標.md) |
| 1841 | Jacobi 的 Jacobian 函數行列式與多重積分變數變換 | [1841-Jacobi行列式.md](1841-Jacobi行列式.md) |
| 1843 | Hamilton 在都柏林橋上刻下四元數 $i^2=j^2=k^2=ijk=-1$ | [1843-Hamilton四元數.md](1843-Hamilton四元數.md) |
| 1844 | Grassmann《擴張論》：n 維向量空間、線性相依、外積 | [1844-Grassmann向量空間.md](1844-Grassmann向量空間.md) |
| 1846 | Jacobi 旋轉消去法：最早的對稱矩陣特徵值數值方法 | [1846-Jacobi特徵值方法.md](1846-Jacobi特徵值方法.md) |
| 1850 | Sylvester 創造 "matrix"（矩陣）一詞 | [1850-Sylvester矩陣命名.md](1850-Sylvester矩陣命名.md) |
| 1851 | Sylvester 慣性定律：二次型的合同分類 $(n_+, n_-, n_0)$ | [1851-Sylvester慣性定律.md](1851-Sylvester慣性定律.md) |

### 矩陣時代（1858–1888）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1858 | Cayley《矩陣論回憶錄》：矩陣代數與 Cayley–Hamilton 定理 $p_A(A)=0$ | [1858-Cayley矩陣代數.md](1858-Cayley矩陣代數.md) |
| 1868 | Weierstrass 初等因子理論，Jordan 標準形的嚴格前奏 | [1868-Weierstrass初等因子.md](1868-Weierstrass初等因子.md) |
| 1870 | Jordan 標準形 $A=PJP^{-1}$，線性變換分類完成 | [1870-Jordan標準形.md](1870-Jordan標準形.md) |
| 1873 | Beltrami 首創奇異值分解雛形 $A=U\Sigma V^T$ | [1873-BeltramiSVD起源.md](1873-BeltramiSVD起源.md) |
| 1878 | Frobenius：矩陣秩、特徵多項式 $\chi_A(\lambda)=\det(\lambda I-A)$ | [1878-Frobenius秩與特徵多項式.md](1878-Frobenius秩與特徵多項式.md) |
| 1883 | Gram 正交化（Schmidt 1907 系統化），QR 與希爾伯特空間前奏 | [1883-GramSchmidt正交化.md](1883-GramSchmidt正交化.md) |
| 1884 | Gibbs 向量分析：點積、叉積、Maxwell 方程的向量語言 | [1884-Gibbs向量分析.md](1884-Gibbs向量分析.md) |
| 1888 | Peano 向量空間公理，線性代數的公理體系 | [1888-Peano向量空間公理.md](1888-Peano向量空間公理.md) |

### 動態與統計（1900–1936）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1900 | Ricci 與 Levi-Civita 張量微積分，廣義相對論的數學引擎 | [1900-Ricci張量微積分.md](1900-Ricci張量微積分.md) |
| 1901 | Pearson 主軸論文：相關矩陣與 PCA 的統計語言 | [1901-Pearson相關與PCA.md](1901-Pearson相關與PCA.md) |
| 1906 | Markov 鏈：轉移矩陣 $P$、穩態分布與 Perron–Frobenius 定理 | [1906-Markov鏈與矩陣.md](1906-Markov鏈與矩陣.md) |
| 1932 | von Neumann 以 Hilbert 空間把線性代數推廣到無窮維 | [1932-VonNeumannHilbert空間.md](1932-VonNeumannHilbert空間.md) |
| 1936 | Eckart–Young 定理：SVD $A=U\Sigma V^T$ 與最佳低秩逼近 | [1936-EckartYoungSVD.md](1936-EckartYoungSVD.md) |
| 1947 | von Neumann–Goldstine 條件數 $\kappa(A)$ 與誤差分析 | [1947-VonNeumann條件數.md](1947-VonNeumann條件數.md) |
| 1944 | Doolittle LU 分解 $A=LU$，Gauss 消去法的程式化 | [1944-DoolittleLU分解.md](1944-DoolittleLU分解.md) |

### 計算與現代（1951–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1951 | Lanczos 迭代法：Krylov 子空間與稀疏矩陣特徵值 | [1951-Lanczos迭代法.md](1951-Lanczos迭代法.md) |
| 1950 | 冪迭代法 $v_{k+1}=Av_k/\|Av_k\|$ 收斂到主特徵值 | [1950-冪迭代法.md](1950-冪迭代法.md) |
| 1954 | Givens 旋轉：平面旋轉消去矩陣元素 | [1954-Givens旋轉.md](1954-Givens旋轉.md) |
| 1958 | Householder 反射與 QR 分解 $A=QR$，數值線性代數誕生 | [1958-HouseholderQR分解.md](1958-HouseholderQR分解.md) |
| 1961 | Francis 雙位移 QR 演算法，特徵值求解的標準 | [1961-FrancisQR演算法.md](1961-FrancisQR演算法.md) |
| 1969 | Strassen 分塊乘法，複雜度 $O(n^{2.807})$ 打破 $O(n^3)$ | [1969-Strassen矩陣乘法.md](1969-Strassen矩陣乘法.md) |
| 1976 | 共軛梯度法被發掘為迭代法，稀疏系統求解主力 | [1976-ConjugateGradient稀疏求解.md](1976-ConjugateGradient稀疏求解.md) |
| 1998 | Google PageRank：Markov 鏈的最大應用 $\pi=\pi P$ | [1998-GooglePageRank.md](1998-GooglePageRank.md) |
| 2006 | 壓縮感知：$\ell_1$ 最小化恢復稀疏訊號 | [2006-壓縮感知.md](2006-壓縮感知.md) |
| 2007 | 隨機化 SVD：$Y=A\Omega$、隨機投影超越古典方法 | [2007-隨機化SVD.md](2007-隨機化SVD.md) |
| 2013 | word2vec 詞向量：$v_{king}-v_{man}+v_{woman}\approx v_{queen}$ | [2013-Word2Vec詞向量.md](2013-Word2Vec詞向量.md) |
| 2016 | 稀疏矩陣與 CSR 格式，Web 規模計算的基礎 | [2016-稀疏矩陣與CSR.md](2016-稀疏矩陣與CSR.md) |
| 2020s | 深度學習線性代數：$y=Wx+b$、注意力 $\operatorname{softmax}(QK^T/\sqrt{d})V$ | [2020s-深度學習線性代數.md](2020s-深度學習線性代數.md) |
| 2024 | 圖神經網路：鄰接矩陣與譜圖理論的訊息傳遞 | [2024-圖神經網路線性代數.md](2024-圖神經網路線性代數.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 前300 | 《九章算術》作者群 | 聯立方程消去法 |
| 1637 | René Descartes | 座標幾何 |
| 1693 | Gottfried Leibniz | 行列式 |
| 1750 | Gabriel Cramer | Cramer 法則 |
| 1772 | Alexandre Vandermonde | 行列式獨立化 |
| 1795 | Carl Friedrich Gauss | 最小平方法 |
| 1787 | Joseph-Louis Lagrange | 二次型化簡 |
| 1812 | Augustin-Louis Cauchy | 行列式乘法規則 |
| 1827 | August Möbius | 重心座標 |
| 1841 | Carl Jacobi | Jacobian、特徵值旋轉法 |
| 1843 | William Hamilton | 四元數 |
| 1844 | Hermann Grassmann | 向量空間、外積 |
| 1850 | James Sylvester | "matrix" 一詞 |
| 1851 | James Sylvester | 慣性定律 |
| 1858 | Arthur Cayley | 矩陣代數、Cayley–Hamilton |
| 1868 | Karl Weierstrass | 初等因子理論 |
| 1870 | Camille Jordan | Jordan 標準形 |
| 1873 | Eugenio Beltrami | SVD 起源 |
| 1878 | Ferdinand Frobenius | 秩、特徵多項式 |
| 1883 | Jørgen Gram / Erhard Schmidt | 正交化 |
| 1884 | Josiah Gibbs | 向量分析 |
| 1888 | Giuseppe Peano | 向量空間公理 |
| 1900 | Ricci / Levi-Civita | 張量微積分 |
| 1901 | Karl Pearson | 相關與 PCA |
| 1906 | Andrey Markov | Markov 鏈 |
| 1932 | John von Neumann | Hilbert 空間 |
| 1936 | Eckart / Young | SVD 低秩逼近 |
| 1944 | Banachiewicz / Doolittle | LU 分解 |
| 1947 | von Neumann / Goldstine | 條件數、誤差分析 |
| 1951 | Cornelius Lanczos | 迭代法 |
| 1954 | Wallace Givens | Givens 旋轉 |
| 1958 | Alston Householder | QR 分解 |
| 1961 | John Francis | QR 演算法 |
| 1969 | Volker Strassen | Strassen 演算法 |
| 1976 | Hestenes / Stiefel（再發掘） | 共軛梯度法 |
| 1998 | Page / Brin | PageRank |
| 2006 | Candès / Tao / Donoho | 壓縮感知 |
| 2007/2011 | Halko / Martinsson / Tropp | 隨機化 SVD |
| 2013 | Tomáš Mikolov | word2vec 詞向量 |
| 2017 | Kipf / Welling | 圖神經網路（GCN） |
| 2020s | 機器學習社群 | GPU、Transformer、LoRA |

## 案件主軸：三幕劇

1. **第一幕：命名**（前300–1850）——從算籌的損益消去到行列式的名字：解聯立方程的需求催生了 $x_i=\det(A_i)/\det(A)$；Hamilton 放棄交換律、Grassmann 看見 n 維空間，為「結構」的思想開路。
2. **第二幕：結構**（1858–1888）——Cayley 的矩陣代數、Jordan 的分類、Frobenius 的秩與特徵多項式、Gibbs 的向量、Peano 的公理：線性代數從「計算工具」升格為「數學結構」。
3. **第三幕：加速**（1906–至今）——Markov 讓矩陣描述隨機、SVD 提煉資訊、Householder 確保數值穩定、Strassen 打破計算量下界；最終矩陣乘法成為 GPU 與 LLM 的心臟。

## 核心數學一覽

- Cramer 法則：$x_i = \dfrac{\det(A_i)}{\det(A)}$
- 最小平方法：$\hat{x} = (A^TA)^{-1}A^Tb$
- 行列式乘法：$\det(AB) = \det(A)\det(B)$
- Cayley–Hamilton：$p_A(A) = 0$，其中 $\chi_A(\lambda)=\det(\lambda I - A)$
- Jordan 標準形：$A = PJP^{-1}$
- SVD：$A = U\Sigma V^T$
- Markov 穩態：$\pi = \pi P$
- Krylov 子空間：$\mathcal{K}_k = \operatorname{span}\{b, Ab, \dots, A^{k-1}b\}$
- Strassen：$O(n^{2.807}) < O(n^3)$
- 注意力機制：$\operatorname{softmax}\!\left(\dfrac{QK^T}{\sqrt{d}}\right)V$
