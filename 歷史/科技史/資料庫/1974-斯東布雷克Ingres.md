# 1974 - Ingres（大學版關聯式資料庫與查詢最佳化）

## 案件摘要
1974–75 年，UC Berkeley 的 **Michael Stonebraker（1943–）**
帶領學生開始開發 **Ingres**（INteractive Graphics REtrieval System）：
$$\boxed{\text{在廉價的 PDP-11 上，證明關聯式資料庫真的可行}}$$
同一時間，IBM 的 System R（見 `1974-錢柏林SQL.md`）在**大公司的資源**下開發；
Ingres 走的是**完全不同的路線**：
- **大學原型**：學生、廉價硬體、開放原始碼；
- **QUEL 語言**：不用 SELECT--FROM--WHERE，而用**元組關聯演算**（tuple calculus）；
- **查詢最佳化**：**選擇下推**（selection pushdown）——先過濾再連接。
$$\text{IBM（資本路線）} \;\parallel\; \text{Berkeley（學術路線）} = \text{關聯式的雙引擎}.$$
**Ingres 證明：關聯式不是 IBM 的專利**——
**這是開放原始碼資料庫血統的起點**，也是 Stonebraker 日後
**2014 年圖靈獎**的立功之地。

## 前因 -- 為什麼會有這個案子
- **Codd 的關聯式模型（1970）**：
  Codd 在 IBM 發表關聯式模型（見 `1970-科德關聯式資料庫.md`）：
  $$\text{資料} = \text{表}，\ \text{查詢} = \text{關聯代數}，\ \text{答案} = \text{表}.$$
  理論上**任何一行代數式都可算出**——
  但**沒有人證明它在真實硬體上跑得動**——
  學界質疑：**「漂亮的數學會不會慢得不能用？」**
- **IBM 內外的冷熱對比**：
  IBM 內部對 Codd 的理論**興趣缺缺**（IMS 網狀資料庫既得利益）；
  但 **Berkeley 的 Stonebraker** 讀了 Codd 的論文後意識到：
  $$\boxed{\text{這是學術界的一次千載難逢的機會——證明它，就名留青史}}$$
  他向 NSF（美國國家科學基金會）申請經費——**大學版資料庫**專案啟動。
- **System R 的競爭對照**：
  IBM 在 1974 年啟動 System R（見 `1974-錢柏林SQL.md`）——
  同一問題、兩種路線：
  $$\text{System R：SEQUEL + 大機器} \quad vs \quad \text{Ingres：QUEL + 小機器}.$$
  兩邊互相**看論文、搶時間、較勁效能**——
  這場競賽**加速了整個資料庫產業的誕生**。
- **QUEL 的理論基礎**：
  Stonebraker 採用 **Codd 的元組關聯演算**（tuple relational calculus）：
  $$\{t \mid \varphi(t)\} \quad\text{（「所有滿足條件 }\varphi\text{ 的元組 }t\text{」）}$$
  Codd 已證明**代數與演算等價**——
  QUEL 選了**演算**這條路，SQL 選了**代數**這條路——殊途同歸。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：QUEL 的元組演算
一個 QUEL 查詢（列出薪水高於 50000 的員工）：
```
range of e is emp
retrieve (e.name) where e.salary > 50000
```
對應元組演算：
$$\{e.\text{name} \mid e \in \text{emp} \wedge e.\text{salary} > 50000\}$$
- `range of e is emp`：宣告變數 $e$ 的範圍（存在量詞的顯式化）；
- `retrieve ... where`：集合建構式 $\{t \mid \varphi(t)\}$；
  $$\boxed{\text{QUEL = 關聯演算的直接實現（比 SQL 更「數學」）}}$$

### 第二條線索：代數等價變換——查詢最佳化的雛形
同一個查詢有**多種代數寫法**，結果相同但**成本天差地遠**：
$$\pi_{name}\big(\sigma_{sal>50000}(\text{emp}) \Join \text{dept}\big) \;=\; \pi_{name}\big((\sigma_{sal>50000}\text{emp}) \Join \text{dept}\big)$$
**選擇下推（$\sigma \downarrow$）**：把選擇**盡量往樹的下方推**——
$$\sigma_{\theta}(A \Join B) \;\xrightarrow{\ \sigma \downarrow\ }\; (\sigma_{\theta_A} A) \Join (\sigma_{\theta_B} B)$$
**為什麼更快？**
- 假設 $|A| = m$、$|B| = n$、選擇條件留下比例 $f$：
  - 先連接再選擇：中間結果 $m \times n$ 行；
  - 先選擇再連接：中結果 $f \cdot m \times f \cdot n$ 行——
  $$\boxed{f^2 \cdot mn \;\ll\; mn \quad\text{（選擇比例越小，省得越多）}}$$

### 第三條線索：Ingres 的「分解式最佳化」
Ingres 的創新：**查詢分解**（query decomposition）——
把**巢狀查詢**拆成**多個簡單的單變數查詢**，逐一處理：
$$Q_{\text{巢狀}} \xrightarrow{\text{Ingres 分解}} Q_1, Q_2, \dots, Q_k \quad(\text{每個只碰一個變數})$$
- 這是**動態規劃式最佳化**的先聲；
- System R 後來發展出**成本基礎最佳化**（cost-based optimizer）——
  兩條路線共同奠定了**現代查詢最佳化器**的基礎：
  $$\text{代數變換（Ingres）} + \text{成本模型（System R）} = \text{現代最佳化器}.$$

### Python：查詢最佳化——先選擇再連接 vs 先連接再選擇

```python
# Toy 資料：員工表 emp 與部門表 dept
emp = [(i, f"員工{i}", (i % 5) * 20000 + 30000, i % 10)
       for i in range(1, 1001)]          # 1000 筆員工，薪水 30000~110000
dept = [(d, f"部門{d}") for d in range(10)]  # 10 個部門

def salary_key(r):
    """薪水欄位的位置：原始 emp 行在 [2]，JOIN 後的行在 [0][2]"""
    return r[2] if isinstance(r[0], int) else r[0][2]

def select_salary_over_90k(rows):
    """σ：選擇薪水 > 90000 的行（留下約 1/5）"""
    return [r for r in rows if salary_key(r) > 90000]

def join(emp_rows, dept_rows):
    """⋈：emp ⋈ dept（笛卡兒積再過濾，比對 dept_id）"""
    dmap = dict(dept_rows)               # 鍵→值映射（JOIN 的本質）
    return [(e, dmap[e[3]]) for e in emp_rows]

# 方法 A：先連接再選擇（壞計畫：1000 × 10 的中間結果）
middle_A = join(emp, dept)               # 中間結果：1000 行（積之後過濾）
result_A = select_salary_over_90k(middle_A)

# 方法 B：先選擇再連接（好計畫：σ↓ 選擇下推，中間結果只剩 200 行）
small_emp = select_salary_over_90k(emp)  # 中間結果：約 200 行
result_B = join(small_emp, dept)

# 成本對比
f = len(small_emp) / len(emp)
print("查詢最佳化：σ↓（選擇下推）的威力")
print(f"  員工表 {len(emp)} 行 × 部門表 {len(dept)} 行")
print(f"  選擇條件 salary > 90000 留下比例 f = {f:.2f}")
print(f"  方法 A（先⋈再σ）：中間結果 {len(middle_A)} 行")
print(f"  方法 B（先σ↓再⋈）：中間結果 {len(small_emp)} 行")
print(f"  理論值 f²·mn = {f**2 * len(emp) * len(dept):.0f}，f·mn ≈ {f * len(emp):.0f}")
print(f"  省下 {len(middle_A) - len(small_emp)} 行中間處理（{(1-f)*100:.0f}% 減量）")
print(f"  兩種方法結果相同嗎？{sorted(result_A) == sorted(result_B)}（{len(result_A)} 筆）")
print("  → 代數等價變換：結果不變，成本大減——Ingres 的核心洞察 ✓")
```
輸出：
```
查詢最佳化：σ↓（選擇下推）的威力
  員工表 1000 行 × 部門表 10 行
  選擇條件 salary > 90000 留下比例 f = 0.20
  方法 A（先⋈再σ）：中間結果 1000 行
  方法 B（先σ↓再⋈）：中間結果 200 行
  理論值 f²·mn = 400，f·mn ≈ 200
  省下 800 行中間處理（80% 減量）
  兩種方法結果相同嗎？True（200 筆）
  → 代數等價變換：結果不變，成本大減——Ingres 的核心洞察 ✓
```

## 結案 -- 後果與影響
- **開放原始碼的先驅（1970s）**：
  Ingres 以**象徵性費用**授權給任何申請者——
  約有**上千個單位**拿到原始碼——
  $$\text{Ingres 原始碼} \xrightarrow{\text{散佈}} \text{開源資料庫的血統起點}.$$
  這是 UNIX 之外，**大學軟體散佈模式**的又一成功案例
  （見 `../資訊科學/1973-UNIX作業系統.md`）。
- **商業血統：Sybase 與 SQL Server**：
  - **Sybase（1984）**：由 Ingres 團隊成員創立——承襲 Ingres 的技術血統；
  - **MS SQL Server（1989）**：微軟與 Sybase 合作——**SQL Server 的祖先是 Ingres**！
  $$\text{Ingres（Berkeley）} \to \text{Sybase（1984）} \to \text{MS SQL Server（1989）}.$$
- **QUEL vs SQL 之爭**：
  - QUEL：**更理論化**（元組演算）、有**型別檢查**、無「SQL 方言混亂」；
  - SQL：**更商業化**（IBM 背書）、語法簡單、**生態系統龐大**；
  $$\text{1980s：QUEL 輸給 SQL} \xrightarrow{\text{原因：IBM 的市場力量 + SQL 標準化}} \text{SQL 統一}.$$
  **技術上更好的語言不見得贏**——這是軟體史的重要教訓。
- **Postgres（1986）**：
  Stonebraker 在 Ingres 之後啟動 **Postgres**
  （POST-Ingres，加入物件概念，見 `1986-波斯特Postgres.md`，稍後建立）——
  它後來變成 **PostgreSQL**——**至今最強的開源關聯式資料庫**。
- **Stonebraker 2014 圖靈獎（伏筆）**：
  $$\boxed{\text{2014 年 ACM 圖靈獎：表彰他對「資料庫事務處理系統」的貢獻}}$$
  從 Ingres（1974）到圖靈獎（2014）——**四十年**的學術長跑；
  他也是 **C-Store（Vertica）、H-Store（VoltDB）** 等多家公司的創辦人。
- **理論與產業的雙贏**：
  $$\text{Codd 理論（1970）} \to \begin{cases} \text{System R（1974）} \to \text{Oracle/DB2} \\ \text{Ingres（1974）} \to \text{Postgres/SQL Server} \end{cases}$$
  **兩條路線共同證明**：關聯式模型是**可行、高效、可商用**的——
  這個驗證讓整個資料庫產業在 1980 年代**全面轉向關聯式**。
- 歷史定位：**Ingres 是「學術原型改變產業」的典範**——
  一群學生在廉價硬體上寫出的系統，
  $$\text{廉價 PDP-11（1974）} \xrightarrow{\text{四十年}} \text{雲端時代的 PostgreSQL（2026）}.$$

## 關鍵人物與文獻
- **M. Stonebraker**：Ingres（1974–75，與 E. Wong、G. Held 等合作）；Postgres（1986）；2014 圖靈獎。
- **E. Wong**、**G. Held**、**P. Kreps**：Ingres 核心開發者；*The Design and Implementation of INGRES*（1976）。
- **E. F. Codd**：關聯式模型（1970）與元組關聯演算——Ingres 的理論基礎。
- **D. Chamberlin & R. Boyce**：SEQUEL（1974）——System R 的競爭對照。
- 相關案件：`1936-圖靈機.md`、`1970-科德關聯式資料庫.md`、`1974-錢柏林SQL.md`、`1979-甲骨文ORACLE.md`、`1986-波斯特Postgres.md`。
