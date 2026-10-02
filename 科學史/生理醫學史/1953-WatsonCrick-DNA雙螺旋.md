# 1953 - Watson 與 Crick 的 DNA 雙螺旋（遺傳物質的讀寫格式現形）

## 案件摘要
1953 年 4 月，James Watson 與 Francis Crick 在《Nature》發表一篇**僅一頁**的論文：
DNA 的**雙螺旋結構**——兩條反向平行的骨架，鹼基 A-T、G-C 成對配對，
$$\text{A}-\text{T}, \qquad \text{G}-\text{C} \qquad (\text{華生-克里克配對}).$$
一頁、無實驗數據（數據來自 Franklin 的 X 射線繞射），卻偵破了
「遺傳資訊儲存在哪、如何複製」的世紀之謎——**遺傳物質有了讀寫格式。**
（1962 年諾貝爾生理醫學獎。）

## 前因 -- 為什麼會有這個案子
- **DNA 的翻身（1944–1952）**：1943 年前主流認為遺傳物質是**蛋白質**（20 種胺基酸，
  比 DNA 的 4 種鹼基「更有資訊量」）。但 Avery（1944）的轉型實驗證明**DNA 就是轉型因子**；
  Hershey–Chase（1952）用放射性標記 ($^{32}$P vs $^{35}$S) 確認——**蛋白質是兇手的幻影，DNA 才是主角。**
- **X 射線繞射的線索**：倫敦國王學院的 Rosalind Franklin 與 Maurice Wilkins 拍出
  高品質的 DNA 纖維繞射照片——**Photo 51** 清晰顯示螺旋與 34 Å 螺距、3.4 Å 層距。
- **Watson 的偵探直覺**：他看懂了 Photo 51（Franklin 本人尚未發表就看出）：
  **螺旋是雙股的，骨架在外面，鹼基在裡面**。Crick（物理學家）補上數學：
  繞射圖樣的螺旋變換（Cochran–Crick–Vand 理論）+ 碱基配對的氫鍵幾何。

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：Photo 51 的幾何解讀
X 射線繞射圖樣的關鍵特徵：
- **十字形斑點** = 螺旋的指紋（Cochran–Crick–Vand 方程的預言）
- **強子午線反射 @ 3.4 Å** = 鹼基堆疊間距
- **強赤道反射 @ 20 Å** = 螺旋直徑
- **缺失的第 4 層線** = **雙股螺旋**（單股會出現）

$$\text{螺距} = 34 \text{ Å} = 10 \times 3.4 \text{ Å（每轉 10 個鹼基）}.$$

### 核心推理二：鹼基配對 = 複製機制
Crick 的最大洞見：**配對就是複製**。A-T（2 氫鍵）、G-C（3 氫鍵），
骨架反向平行：
$$5'-\text{A T G C}-3' \quad \Big\| \quad 3'-\text{T A C G}-5'.$$
複製時雙鏈解開，每股當模板按配對規則合成新股——**半保留複製**
（1958 年 Meselson–Stahl 用 $^{15}$N 同位素實驗證實）。
**這是分子生物學的中心法則的起點**：DNA → RNA → 蛋白質。

### Python：互補配對與半保留複製的模擬

```python
COMPLEMENT = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}

def replicate(dna):
    # 半保留複製：每股當模板，按配對規則合成新股
    return [''.join(COMPLEMENT[b] for b in dna),      # 新股 1（對舊股 1）
            ''.join(COMPLEMENT[b] for b in dna[::-1])]  # 反向平行股

def gc_content(dna):
    return (dna.count('G') + dna.count('C')) / len(dna)

dna = "ATGCCGTAAGCTTACGGCATTACCGGT"
new1, new2 = replicate(dna)
print("原股 :", dna)
print("新股1:", new1, "（互補）")
print("GC 含量:", f"{gc_content(dna)*100:.1f}%")
# 驗證：複製後的兩條雙螺旋與原版完全相同
print("複製正確:", all(COMPLEMENT[a]==b for a,b in zip(dna,new1)))
```
輸出：
```
原股 : ATGCCGTAAGCTTACGGCATTACCGGT
新股1: TACGGCATTCGAATGCCGTAATGGCCA（互補）
GC 含量: 51.9%
複製正確: True
```

### 雙螺旋的偵查證據鏈
| 證據 | 提供者 | 推理 |
|------|--------|------|
| Photo 51 的十字斑點 | Franklin | 螺旋結構 |
| 3.4 Å / 34 Å 層距 | Franklin/Wilkins | 鹼基堆疊與螺距 |
| Char–Gaff 定則（A=T, G=C） | Chargaff (1950) | 鹼基配對 |
| 轉型實驗 | Avery (1944) | DNA 是遺傳物質 |
| 模型搭建 | Watson–Crick | 雙股 + 反向平行 + 配對 |

**Chargaff 定則的偵探意義**：任何 DNA 中 A 的量 = T 的量、G = C——
這是「鹼基成對」的化學線索，Watson–Crick 的配對規則直接解釋了它。

## 結案 -- 後果與影響
- **分子生物學的誕生**：DNA 雙螺旋成為分子生物學的中心——
  中心法則（DNA→RNA→蛋白質）、遺傳密碼（1966, Nirenberg）、
  基因工程（1973）全部建立在雙螺旋之上。
- **遺傳密碼的破解**：雙螺旋 + mRNA → 1966 年 Nirenberg 破解 64 個密碼子——
  **生命的語言被讀出**（Sanger 定序，見 `1977-Sanger定序法.md`，是下一章）。
- **Franklin 的公道**：Franklin 1958 年死於癌症（38 歲），未及領獎——
  諾獎不頒給死者，她的貢獻被淡化數十年。**今日 Photo 51 的功勞已歸還給她**——
  發明模型的名聲屬於 Watson–Crick，**數據的主角屬於 Franklin**。
- **醫學的後果**：基因檢測、基因治療、CRISPR（見 `2012-CRISPR基因編輯.md`）——
  **讀寫生命的格式，從這一頁論文開始。**
- 半保留複製的驗證：Meselson–Stahl (1958) 用 $^{15}$N 實驗——
  被稱為「生物學史上最美的實驗」。

## 關鍵人物與文獻
- **J. D. Watson & F. H. C. Crick**：Nature 171, 737 (1953)。
- **Rosalind Franklin & Maurice Wilkins**：X 射線繞射數據（國王學院）。
- **O. T. Avery**：轉型實驗 (1944)；**Hershey–Chase**：放射性標記 (1952)；**Chargaff**：定則 (1950)。
- 相關案件：`1865-Mendel豌豆遺傳.md`、`1977-Sanger定序法.md`、`2012-CRISPR基因編輯.md`。
