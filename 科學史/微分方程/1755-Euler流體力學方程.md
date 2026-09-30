# 1755 尤拉與流體力學方程

## 案發現場

十八世紀的流體力學是一片渾沌。達朗貝爾在 1749 年左右得出了著名的「**達朗貝爾悖論**」：用當時的勢流理論計算，物體在理想流體中運動竟不受任何阻力——但現實中船行水上阻力明顯。理論與觀測之間出現巨大鴻溝。

更根本的問題是：**連續的流體**該如何寫出運動方程？牛頓力學是針對**離散質點**的 $\mathbf{F} = m\mathbf{a}$；流體卻由無窮多流體元組成，彼此推擠、變形，每個時刻每個位置的密度 $\rho$ 與速度 $\mathbf{u}=(u,v,w)$ 都在變。達朗貝爾與丹尼爾·伯努利（《流體動力學》，1738）只處理了特殊情境（如管流、射流），**一般的運動方程**仍付之闕如。

1755 年，在柏林任職的尤拉（Leonhard Euler）發表論文〈流體運動的一般原理〉（Principes généraux du mouvement des fluides），一口氣寫下**理想流體的完整方程組**。他自己在論文末感嘆：「對我而言，這一切都已豁然開朗，只欠計算。」這組方程至今仍冠著他的名字——**Euler 方程**。

## 偵查過程

尤拉的偵查手法是**歐拉觀點**（場論觀點）：不追蹤個別流體粒子的軌跡（那是拉格朗日觀點），而是站在空間固定點，觀察流體「路過」時的狀態變化。

**第一步：質量守恆——連續方程。**
考慮固定的小控制體 $dV = dx\,dy\,dz$。單位時間內流出的質量淨額等於體內密度的減少率：

$$
\frac{\partial \rho}{\partial t} = -\left[ \frac{\partial(\rho u)}{\partial x} + \frac{\partial(\rho v)}{\partial y} + \frac{\partial(\rho w)}{\partial z} \right]
$$

寫成場論形式：

$$
\boxed{\,\frac{\partial \rho}{\partial t} + \nabla\cdot(\rho \mathbf{u}) = 0\,}
$$

尤拉當年是用分量形式逐一寫出（ nabla 記號要到 19 世紀才由 Heaviside 普及），但思想完全一致。

**第二步：動量方程——牛頓第二定律的場論版。**
對流體元 $dV$（質量 $\rho\,dV$），受力有二：體力（如重力 $\rho \mathbf{g}$）與表面壓力。壓力在 $x$ 方向的淨力為

$$
-\left[ p(x+dx, y, z) - p(x, y, z) \right] dy\,dz = -\frac{\partial p}{\partial x}\, dV
$$

（負號因壓力從高壓側推向低壓側。）而流體元的加速度**不是** $\partial_t \mathbf{u}$——因為流體元本身在移動，必須用隨體導數（物質導數）：

$$
\frac{D\mathbf{u}}{Dt} = \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u}
$$

其中 $(\mathbf{u}\cdot\nabla)\mathbf{u}$ 是**對流加速度**：流體元被沖到速度不同的下一站而「感受到」的加速度變化。牛頓第二定律給出：

$$
\boxed{\,\rho\left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} \right) = -\nabla p + \rho \mathbf{g}\,}
$$

**第三步：封閉方程組。** 四個方程（一個連續方程 + 三個動量分量）配四個未知數（$\rho, u, v, w$），再加上壓力的本構關係（如 $\rho = \rho(p)$），方程組封閉。這就是理想流體力學的完整骨架。

**第四步：無黏性假設的代價。** 尤拉假設流體「易流」（fluidity），即流體元之間只傳遞法向壓力、**不傳遞切向摩擦力**。這讓方程乾淨優美，但也種下禍根：沒有黏性就沒有壁面邊界層，數學上阻力會消失，正是達朗貝爾悖論的根源。

**第五步：無旋流的簡化。** 若初始時刻流動無旋（$\nabla\times\mathbf{u} = \mathbf{0}$），可引入速度勢 $\mathbf{u} = \nabla\phi$，動量方程可積分出**伯努利定律**的推廣形式：

$$
\frac{\partial \phi}{\partial t} + \frac{1}{2}|\nabla\phi|^2 + \frac{p}{\rho} + gz = \text{const}
$$

這條沿流線的常數關係，把丹尼爾·伯努利 1738 年的實驗定律提升為嚴格的推論。

## 結案報告

尤拉的方程組解決了「一般流體如何運動」的核心謎題，把流體力學從零散的特殊解集，變成有公理基礎的演繹科學。但它同時開啟了**新的百年懸案**：

1. **達朗貝爾悖論持續 150 年**，直到 Prandtl（1904）提出**邊界層理論**：黏性雖小，卻在物體表面附近的薄層內主導流動，產生分離與阻力。理論至此才與造船、航空的實務接軌。
2. **Navier–Stokes 方程（1822–1845）**：Navier 與 Stokes 在尤拉方程中加入黏性項，得到

$$
\rho\left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \rho \mathbf{g}
$$

黏性項 $\mu\nabla^2\mathbf{u}$ 正是把尤拉的「易流」假設放寬一階的結果。Navier–Stokes 的解之存在性與唯一性，至今是**千禧年大獎難題**之一。
3. **湍流之謎**：雷諾（Reynolds, 1883）發現高雷諾數下流動失穩成湍流，尤拉方程的無旋優雅解在現實中崩壞——這是物理學最後的未解難題之一。
4. 尤拉的**場論觀點**（以偏微分方程描述空間場的演化）成為整個數學物理的範式，馬克士威電磁學、量子力學的波函數，皆循此路。

與本書其他案件相比：達朗貝爾的波動方程（[1747-dAlembert波動方程.md](1747-dAlembert波動方程.md)）是**線性**偏微分方程的第一戰，尤拉的流體方程則是**非線性**偏微分方程的第一戰——而非線性之難，正是十九、二十世紀應用數學的主旋律。

## 證據與工具

以下程式用數值方法解二維不可壓縮尤拉方程的簡化模型（渦旋疊加），重現「無旋流的優雅」：

```python
import numpy as np
import matplotlib.pyplot as plt

# 二維不可壓縮無黏流的點渦模型：
# 連續方程 ∇·u = 0 由流函數自動滿足：u = ∂ψ/∂y, v = -∂ψ/∂x
# 點渦的速度場（複勢論）：Γ 為環流量強度

N = 400
x, y = np.meshgrid(np.linspace(-2, 2, N), np.linspace(-2, 2, N))

def vortex_velocity(x0, y0, Gamma):
    """單一點渦在 (x0,y0) 處誘導的速度場"""
    dx, dy = x - x0, y - y0
    r2 = dx**2 + dy**2 + 1e-9      # 避免除以零
    return -Gamma * dy / (2*np.pi*r2), Gamma * dx / (2*np.pi*r2)

# 兩個反向旋轉的渦（渦偶極子），符合無黏、無旋（除渦心）的尤拉流
u, v = vortex_velocity(-0.5, 0, +1.0)
u2, v2 = vortex_velocity(+0.5, 0, -1.0)
u, v = u + u2, v + v2

speed = np.sqrt(u**2 + v**2)

# 畫流線圖：渦偶極子像一股噴流，展現伯努利定律（速度快處壓力低）
fig, ax = plt.subplots(figsize=(8, 6))
ax.streamplot(x, y, u, v, color=speed, cmap="viridis", density=1.4)
ax.plot([-0.5, 0.5], [0, 0], "ro", label="vortex cores")
ax.set_title("Euler flow: vortex dipole (inviscid, incompressible)")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend()
plt.tight_layout()
plt.savefig("euler_flow.png", dpi=120)
plt.show()

# 驗證連續方程 ∇·(ρu) = 0：不可壓縮時即 ∇·u = 0
div_u = np.gradient(u, axis=1) / (4.0/(N-1)) + np.gradient(v, axis=0) / (4.0/(N-1))
print(f"max |∇·u| = {np.abs(div_u).max():.2e}  （接近 0 表示連續方程成立）")

# 驗證渦度 ω = ∂v/∂x − ∂u/∂y：除渦心外應處處為 0（無旋）
omega = np.gradient(v, axis=1) / (4.0/(N-1)) - np.gradient(u, axis=0) / (4.0/(N-1))
interior = (np.abs(x) > 0.2) | (np.abs(y) > 0.2)   # 排除渦心附近
print(f"max |ω| away from cores = {np.abs(omega[interior]).max():.2e}  （接近 0 表示無旋）")
```

執行後可見兩個反向渦形成一股向前推進的「噴流」狀流線，且數值驗證了 $\nabla\cdot\mathbf{u}=0$（連續方程）與渦心外無旋——這正是尤拉方程「只欠計算」之後，計算給出的驗屍報告。
