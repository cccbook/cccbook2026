# 1962 — Manchester Atlas 與虛擬記憶體的誕生

## 案件摘要
1962 年，英國 Manchester 大學的 Atlas 電腦首度引入「虛擬記憶體」與「一級儲存」概念：程式以統一位址定址，硬體與作業系統聯手在核心記憶體與磁鼓之間自動搬移資料。這是「程式所見的記憶體 ≠ 實際存在的記憶體」這樁懸案的第一次偵破。

## 前因 -- 為什麼會有這個案子
- 1950 年代末，程式越寫越大，但核心記憶體（磁芯）昂貴且容量小（數萬字），大型資料只能放磁鼓（drum）。
- 傳統做法是「覆蓋（overlay）」：程式設計師自己把程式切成片段，手動載入/換出，錯誤頻繁、無法移植。
- 多程式共用一台機器後，還需要「隔離」與「自動管理」：不能讓 A 程式碰 B 程式的位址，也不能要求程式設計師知道機器有幾 KB。
- 線索：能不能讓硬體把「程式使用的位址」和「記憶體實際位址」分開，由 OS 自動調度？

## 線索與推理 -- 數學式、程式、理論

### 1. 分頁（paging）與需求分頁（demand paging）
把虛擬位址空間切成固定大小的「頁」（Atlas 頁大小 512 字），物理記憶體切成同大小的「頁框」（frame）。程式只在真正用到某頁時才載入它——這就是需求分頁。

$$VA = (p, d) \quad\text{虛擬頁號 } p,\ \text{頁內位移 } d$$

$$PA = f(p) \times (\text{frame size}) + d$$

頁表（page table）記錄每頁的頁框號與「在場位元」（present bit）；不在場時觸發 page fault，由 OS 從磁鼓載入。

### 2. 位址轉換 $VA \to PA$ 與 TLB
Atlas 硬體首次提供位址轉換硬體，並用小型高速關聯暫存器快取最近的轉換——這正是今日 TLB（Translation Lookaside Buffer）的祖先。

$$\text{TLB hit rate} = h \Rightarrow \text{平均轉換時間} = h \cdot t_{TLB} + (1-h)(t_{TLB} + t_{PT})$$

### 3. 置換演算法與 Belady 反常
記憶體滿了要換頁時，誰該被犧牲？
- **FIFO**：換最早進來的頁，實作簡單。
- **LRU**（Least Recently Used）：換最久沒被使用的頁，基於「時間局部性」假設。

Belady（1966）發現驚人反例：FIFO 在某些存取序列下，**頁框越多反而缺頁越多**，即 Belady 反常（anomaly）。LRU 屬於「堆疊演算法」，滿足

$$P_n(k) \subseteq P_n(k+1)$$

（$k$ 個頁框時的常駐頁集是 $k+1$ 個時的子集），因此不會有 Belady 反常。

### 4. 有效存取時間（EAT）
缺頁率 $p$、記憶體存取時間 $t_{mem}$、缺頁服務時間 $t_{fault}$ 時：

$$EAT = (1-p)\times t_{mem} + p \times t_{fault}$$

若 $t_{mem}=100\text{ns}$、$t_{fault}=10\text{ms}$，則只要 $p > 10^{-5}$，EAT 就暴增一倍以上——「缺頁率必須極小」是虛擬記憶體可行的數學底線。

### 5. Python 模擬：LRU 與 Belady 反常

```python
from collections import deque

def fifo(refs, frames):
    mem, queue, faults = set(), deque(), 0
    for r in refs:
        if r not in mem:
            faults += 1
            if len(mem) == frames:
                mem.remove(queue.popleft())
            mem.add(r); queue.append(r)
    return faults

def lru(refs, frames):
    mem, last, faults = set(), {}, 0
    for i, r in enumerate(refs):
        if r not in mem:
            faults += 1
            if len(mem) == frames:
                victim = min(mem, key=lambda x: last[x])
                mem.remove(victim)
            mem.add(r)
        last[r] = i
    return faults

# Belady 反常序列（經典例子）
seq = [1,2,3,4,1,2,5,1,2,3,4,5]
for k in (3, 4):
    print(f"frames={k}: FIFO={fifo(seq,k)}, LRU={lru(seq,k)}")
# 輸出: frames=3: FIFO=9, LRU=10
#       frames=4: FIFO=10, LRU=8   <-- FIFO 反常: 3->4 框缺頁反增
```

## 結案 -- 後果與影響
- Atlas 的「one-level store」成為所有現代作業系統（Multics、Unix、Windows、Linux）虛擬記憶體的直接源頭。
- 分頁 + 需求分頁 + 置換演算法成為 OS 課程的標準章節；TLB 成為 CPU 必備元件。
- 證明了「軟硬體共同設計」的力量：沒有硬體位址轉換，純軟體的虛擬記憶體慢到不可用。
- 虛擬記憶體也是後續「系統虛擬化」的基石：VM/370 與 hypervisor 都建立在位址轉換之上。

## 關鍵人物與文獻
- **Tom Kilburn、D. B. G. Edwards、M. F. Summers**：Manchester Atlas 團隊。
- Kilburn et al., *One-Level Storage System*, IRE Trans. EC-11, 1962.
- L. A. Belady, *A Study of Replacement Algorithms for a Virtual-Storage Computer*, IBM Systems Journal, 1966.
- Denning, *Virtual Memory*, ACM Computing Surveys, 1970.
