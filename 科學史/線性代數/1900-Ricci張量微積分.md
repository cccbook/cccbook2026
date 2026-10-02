# 1900 — Ricci 張量微積分

## 案件摘要
1900 年，Gregorio Ricci-Curbastro 與他的學生 Tullio Levi-Civita 發表《Méthodes de calcul différentiel absolu et leurs applications》（絕對微分法），把線性代數的下標語言推廣到彎曲空間：**張量** $T^i_{\ j}$ 帶著協變與反變指標，在任意座標變換下按明確法則變換，使幾何與物理定律擺脫座標的束縛。這套「絕對微分法」十五年後成為廣義相對論的數學引擎——一樁為 Einstein 預備兇器的世紀大案。

## 前因 -- 為什麼會有這個案子
- **Gauss 1827**：《曲面概論》用第一、第二基本形式 $g_{ij}$、$b_{ij}$ 描述曲面，證明 Gauss 曲率 $K$ 是內在的（Theorema Egregium）——但他的計算繫於特定參數化，換座標就要重算。
- **Riemann 1854**：Riemann 在就職演說〈論幾何學基礎的假說〉中把 Gauss 推廣到 $n$ 維流形，引入度量 $ds^2 = g_{ij}\, dx^i dx^j$ 與曲率張量 $R^i_{\ jkl}$——但原文無人讀懂，公式以座標分量形式寫下，龐雜難用。
- **Christoffel 1869**：Christoffel 發明**Christoffel 符號**
  $$\Gamma^k_{\ ij} = \frac{1}{2} g^{kl}\left(\frac{\partial g_{li}}{\partial x^j} + \frac{\partial g_{lj}}{\partial x^i} - \frac{\partial g_{ij}}{\partial x^l}\right)$$
  並給出協變微分的雛形——這是破案的第一條實質線索。
- **不變式理論的氛圍**：Sylvester、Cayley 的不變式運動席捲代數界；Ricci 問：微分幾何能否也有自己的「不變式」——在座標變換下不變的微分運算？
- Ricci 在帕多瓦大學浸淫 Riemann 與 Christoffel 十餘年（1884 年起），逐步將散落的公式整理成系統。

## 線索與推理 -- 數學式、程式、理論

### 線索一：協變與反變指標——張量的身分證
Ricci 的核心發明：區分**反變指標**（上標，$v^i$，向量）與**協變指標**（下標，$\omega_i$，餘向量/一次形式）。在座標變換 $x^i \to x^{i'}$ 下：

$$v^{i'} = \frac{\partial x^{i'}}{\partial x^i} v^i, \qquad \omega_{i'} = \frac{\partial x^i}{\partial x^{i'}} \omega_i$$

一般張量 $T^{i_1 \dots i_p}_{\ j_1 \dots j_q}$ 每個上標按前者、每個下標按後者變換。**張量方程在任意座標變換下形式不變**——這就是「絕對」（absolu）一詞的含義：定律不依賴座標。

### 線索二：協變微分——讓張量能求導
普通偏導數 $\partial_j v^i$ 不是張量（多出 Christoffel 符號的項）。Ricci 定義**協變導數**：

$$\nabla_j v^i = \partial_j v^i + \Gamma^i_{\ jk} v^k, \qquad \nabla_j \omega_i = \partial_j \omega_i - \Gamma^k_{\ ji}\, \omega_k$$

法則：每個上標加 $\Gamma$ 項、每個下標減 $\Gamma$ 項。如此 $\nabla_j v^i$ 是真正的 $(1,1)$ 張量。度量的協變導數恆為零：

$$\nabla_k g_{ij} = 0$$

這表示協變微分與度量相容——平行移動保持內積。Ricci 用這套記號把 Riemann 曲率寫成：

$$R^i_{\ jkl} = \partial_k \Gamma^i_{\ jl} - \partial_l \Gamma^i_{\ jk} + \Gamma^i_{\ km}\Gamma^m_{\ jl} - \Gamma^i_{\ lm}\Gamma^m_{\ jk}$$

並證明 Ricci 恆等式 $\nabla_{[k} \nabla_{l]} v^i = \frac{1}{2} R^i_{\ jkl} v^j$：**協變導數不對易的程度，就是空間彎曲的程度**。

### 線索三：Einstein 求和約定——記號的最後一次淬鍊
Ricci 原文寫 $\sum_i$，冗長繁瑣。1916 年 Einstein 在廣義相對論論文中引入約定：**同一項中一上一下重複的指標，自動求和**：

$$ds^2 = g_{ij}\, dx^i dx^j \quad \equiv \quad \sum_{i,j} g_{ij}\, dx^i dx^j$$

Einstein 甚至在自傳中半開玩笑地說，這是他對數學的貢獻。求和約定讓張量計算簡潔到物理學家敢用——Levi-Civita 1917 年的平行移動幾何詮釋又補上最後一塊直觀。

### 程式碼範例：2D 球面度量的 Christoffel 符號與 Ricci 曲率
```python
import numpy as np

# 2D 球面（半徑 R=1）：座標 (θ, φ)，ds² = dθ² + sin²θ dφ²
def g_sph(th):        # 度量張量 g_ij(θ)
    return np.array([[1.0, 0.0], [0.0, np.sin(th)**2]])

def g_inv(th):        # 逆度量 g^ij
    return np.linalg.inv(g_sph(th))

R = 1.0
# 唯一非零的 Christoffel 符號（i,j,k ∈ {0:θ, 1:φ}）：
#   Γ^θ_{φφ} = -sinθ cosθ,  Γ^φ_{θφ} = Γ^φ_{φθ} = cotθ
def Gamma(i, j, k, th):
    if (i, j, k) == (0, 1, 1):
        return -np.sin(th) * np.cos(th)
    if (i, j, k) in [(1, 0, 1), (1, 1, 0)]:
        return np.cos(th) / np.sin(th)
    return 0.0

# 用公式驗證：Γ^k_{ij} = ½ g^{kl}(∂_j g_{li} + ∂_i g_{lj} - ∂_l g_{ij})
def dg(l, i, j, th, h=1e-6):   # ∂_l g_ij（此例只有 θ 方向會變）
    t1 = g_sph(th + h) if l == 0 else g_sph(th)
    t0 = g_sph(th - h) if l == 0 else g_sph(th)
    return (t1[i, j] - t0[i, j]) / (2 * h)

def Gamma_num(k, i, j, th):    # Γ^k_{ij} = ½ g^{kl}(∂_j g_{li} + ∂_i g_{lj} - ∂_l g_{ij})
    ginv = g_inv(th)
    return 0.5 * sum(ginv[k, l] * (dg(j, l, i, th) + dg(i, l, j, th) - dg(l, i, j, th))
                     for l in range(2))

th = np.pi / 3
print("Γ^θ_φφ 解析 =", Gamma(0, 1, 1, th),
      " 數值 =", Gamma_num(0, 1, 1, th))
print("Γ^φ_θφ 解析 =", Gamma(1, 0, 1, th),
      " 數值 =", Gamma_num(1, 0, 1, th))

# Ricci 張量（2D）：R_ij = K g_ij，球面 K = 1/R² = 1
# 驗證：Ricci 標量 R = g^{ij} R_ij = 2（2D 球面）
K = 1.0
Ricci = K * g_sph(th)
print("Ricci 標量 R =", np.trace(g_inv(th) @ Ricci))  # 應為 2
```

輸出顯示：Christoffel 符號的解析式與數值微分一致，2D 球面的 Ricci 標量 $R = 2$——曲率是內在量，與座標選擇無關。

## 結案 -- 後果與影響
- **廣義相對論 1915**：Einstein 苦尋彎曲時空的數學語言多年；1912 年他求助於同學 Marcel Grossmann，才得知 Ricci 的絕對微分法。場方程 $R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$ 完全用張量寫成——絕對微分法是廣義相對論的數學引擎。
- **Levi-Civita 1917**：平行移動的幾何詮釋，讓張量計算有了清晰的幾何圖像。
- **微分幾何現代化**：Ricci 流（Perelman 證 Poincaré 猜想的工具，名字直接紀念 Ricci）、聯絡論、纖維叢，全是這套語言的後代。
- **座標無關的物理**：規範場論、Noether 定理的表述，「物理定律與座標無關」成為現代物理的基本原則。
- Ricci 這個姓氏也被寫進每本廣義相對論教科書：Ricci 張量、Ricci 曲率、Ricci 流。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gregorio Ricci-Curbastro | 案件主嫌：絕對微分法（1900） |
| Tullio Levi-Civita | 合著者；1917 平行移動詮釋 |
| Bernhard Riemann | n 維流形與曲率（1854） |
| Elwin Christoffel | Christoffel 符號（1869） |
| Albert Einstein | 求和約定；把兇器用在引力上（1915） |

- G. Ricci, T. Levi-Civita, *Méthodes de calcul différentiel absolu et leurs applications*, Math. Ann. **54** (1900)。
- E. Christoffel, *Über die Transformation der homogenen Differentialausdrücke zweiten Grades*, Crelle J. **70** (1869)。
- A. Einstein, *Die Grundlage der allgemeinen Relativitätstheorie*, Ann. Phys. **49** (1916)。
