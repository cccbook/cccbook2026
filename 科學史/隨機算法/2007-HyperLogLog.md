# 2007 - HyperLogLog

## 案件摘要
2007 年，Philippe Flajolet、Éric Fusy、Olivier Gandouet 與 Frédéric Meunier 發表《HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm》：**用約 1.5 KB 記憶體，估計十億級集合的基數（不重複元素個數），標準誤差約 2%**。這是隨機統計的極致之作：每個元素只留下一個「最大前導零」的指紋，64 個暫存器就能數出天文數字。HyperLogLog 成為現代大數據基數統計的標準（Redis、Google、Presto 內建）。

## 前因 -- 為什麼會有這個案子
基數估計（cardinality estimation）：十億個 IP 位址流過，問「不重複的有多少個？」精確方法需要 $O(n)$ 記憶體（雜湊表或 bitmap：十億位元 = 125 MB）——大數據下不可行。Flajolet 的問題：**能否用遠小的記憶體估計基數？**

譜系：
- **Flajolet–Martin (1985)**：FM 演算法——元素的雜湊值尾隨零的個數 $k$ 提示基數 $\approx 2^k$
- **LogLog (2003)**：分桶平均改進
- **HyperLogLog (2007)**：調和平均 + 偏差校正，達到理論極限

## 線索與推理 -- 數學式、程式、理論

### 核心直覺：前導零的指紋
把每個元素雜湊成隨機位元串。雜湊值開頭有 $k$ 個零的機率：

$$P(\text{前導零} \ge k) = 2^{-k}$$

**推理**：若基數是 $n$，$n$ 個隨機串中「最大前導零」$\rho_{\max}$ 大約滿足 $n \cdot 2^{-\rho_{\max}} \approx 1$，即：

$$n \approx 2^{\rho_{\max}}$$

一個「最大前導零為 20」的串，暗示基數約 $2^{20} \approx 100$ 萬。**每個元素只留下一個數字（$\rho$ 值），統計最大值就能數出天文數字**。

### HyperLogLog 的設計
單一 $\rho_{\max}$ 變異數太大（單次估計誤差 $\sqrt{\pi/2}$ 級）。HLL 分成 $m = 2^b$ 個桶（用雜湊前 $b$ 位選桶），每桶維護自己的 $\rho_{\max}$。估計用**調和平均**：

$$\hat{E} = \alpha_m \cdot m^2 \cdot \left(\sum_{j=1}^m 2^{-M_j}\right)^{-1}$$

其中 $\alpha_m = \left(m \int_0^\infty \left(\log_2\left(\frac{2+u}{1+u}\right)\right)^m du\right)^{-1}$ 是偏誤校正常數（$\alpha_{64} \approx 0.7213$）。

**標準誤差**：

$$\frac{\sigma}{\hat{E}} \approx \frac{1.04}{\sqrt{m}}$$

$m = 2^{14} = 16384$ 個桶時誤差約 0.8%，記憶體 $16384 \times 6$ 位元 = 12 KB。**$m = 2^6$ 桶時 1.5 KB 誤差約 13%。**

### 程式碼：HyperLogLog

```python
import random, hashlib, math

class HyperLogLog:
    def __init__(self, b=14):                 # 2^14 桶，誤差 ~0.8%
        self.b, self.m = b, 1 << b
        self.M = [0] * self.m
        self.alpha = 0.7213 / (1 + 1.079 / self.m)

    def _rho(self, h):
        """h 的前導零個數 + 1（跳過前 b 位選桶用）"""
        rest = h >> self.b
        rho = 1
        while rest & 1 == 0 and rho < 64:
            rest >>= 1; rho += 1
        return rho

    def add(self, item):
        h = int(hashlib.md5(str(item).encode()).hexdigest(), 16)
        j = h & (self.m - 1)                  # 前 b 位選桶
        self.M[j] = max(self.M[j], self._rho(h))

    def count(self):
        est = self.alpha * self.m**2 / sum(2**(-x) for x in self.M)
        if est <= 2.5 * self.m:               # 小基數線性計數校正
            zeros = self.M.count(0)
            if zeros:
                est = self.m * math.log(self.m / zeros)
        return est

random.seed(42)
hll = HyperLogLog(b=14)
true_set = set()
for _ in range(1000000):
    e = random.getrandbits(40)
    hll.add(e); true_set.add(e)

print(f"真實基數 = {len(true_set)}")
print(f"HLL 估計 = {hll.count():.0f}")
# 誤差 ~1%，記憶體僅 12 KB（vs 精確 set 的數十 MB）
```

### 合併性：分散式統計的關鍵
HLL 的殺手級性質：**兩個 HLL 可合併**（每桶取 max）：

$$M_{A \cup B}[j] = \max(M_A[j], M_B[j])$$

合併後的 HLL 恰好估計並集的基數——**分散式系統的每台機器各自維護 HLL，最後合併**。這使 HLL 成為分散式大數據的完美統計工具。

### 譜系的推進
- **FM (1985)**：單一 $\rho$，誤差大
- **LogLog (2003)**：分桶，$m$ 桶誤差 $1.3/\sqrt{m}$
- **HLL (2007)**：調和平均 + 校正，誤差 $1.04/\sqrt{m}$——**理論極限（信息論下界）**

**偵探筆記**：HLL 的推理鏈是「統計放大」——單次觀察（一個 $\rho$ 值）噪聲大，$m$ 個桶的調和平均噪聲 $\propto 1/\sqrt{m}$。與蒙地卡羅（見 `1946-Ulam蒙地卡羅.md`）的 $1/\sqrt{N}$ 誤差、CMS 的 $(1/2)^d$ 同源：**獨立重複是對抗噪聲的免費午餐**。

## 結案 -- 後果與影響
- **大數據標配**：Redis（PFADD/PFCOUNT）、Google BigQuery、Presto/Trino、Spark 內建 HLL。
- **網路監控**：獨立訪客（UV）統計、DDoS 偵測的獨立源計數。
- **資料庫**：查詢優化器的基數估計（JOIN 次序優化的核心）。
- **sketch 學科**：與 CMS（見 `2005-CountMinSketch.md`）、MinHash（見 `1997-BroderMinHash.md`）共同構成概要算法的三大支柱。
- **組合分析**：Flajolet 學派的分析組合學（Analytic Combinatorics）把漸進分析推到極致。

## 關鍵人物與文獻
- **Philippe Flajolet**（1948–2011）：INRIA；分析組合學大師、FM 演算法 (1985)、HLL (2007)
- **Éric Fusy, Olivier Gandouet, Frédéric Meunier**：HLL 共同作者
- Flajolet et al.: HyperLogLog (2007, AofA)
- **Durand & Flajolet**：LogLog (2003)
- **Heule, Nunkesser, Hall**：HLL++ (2013)——工程改進（Google）
- 交叉參照：`1946-Ulam蒙地卡羅.md`、`2005-CountMinSketch.md`、`1997-BroderMinHash.md`
