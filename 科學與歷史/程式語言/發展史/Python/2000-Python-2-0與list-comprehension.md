# 2000：Python 2.0 與 list comprehension——循環垃圾回收與列表推導式

## 事件
2000 年 10 月，**Python 2.0** 發佈，這是 Python 由 **BeOpen / PythonLabs**（Guido 團隊離開 CNRI 後）發佈的第一版，也是社群提案流程 **PEP（Python Enhancement Proposal）** 制度化的開始。三大新特性：

1. **列表推導式（list comprehension）**（PEP 202）：`[x*x for x in xs if x > 0]`
2. **循環垃圾回收（cyclic garbage collector）**（PEP 205）
3. **擴充指定運算子** `+=`、`*=`（PEP 203），以及 Unicode 字串型別 `unicode`

## 為何重要
- **PEP 制度**：從 2.0 開始，所有重大變更都要寫 PEP 提案、公開討論、由 BDFL（仁慈的終身獨裁者，即 Guido）裁決——Python 的演進從此有治理結構。
- **列表推導式**是 Python 語法史上最成功的添加之一，日後成為「Pythonic」風格的代名詞。
- **循環垃圾回收**是記憶體管理從「純引用計數」走向混合式回收的轉捩點。

## 理論與實用原因
- **理論原因（列表推導式）**：源自 **SETL（1970）** 與 **Haskell（1990）** 的集合建構式（set comprehension）數學記法。理論上，宣告式「描述要什麼」比命令式「描述怎麼做」更接近數學、更不易出錯——沒有索引變數就沒有 off-by-one 錯誤。
- **理論原因（循環 GC）**：純**引用計數**（reference counting，繼承自 1960 年代 Lisp 實作）無法回收**循環引用**（`a.b = b; b.a = a`）。2.0 加入 mark-and-sweep 式的循環偵測器（基於 1960 年 McCarthy 的追蹤式回收理論），與引用計數並存——小物件靠計數即時釋放、循環靠週期性掃描。
- **實用原因**：Unicode 型別是為了應對 1990 年代末網際網路時代的多語系文字（ASCII 不夠用）；`+=` 是為了減少 `x = x + 1` 的樣板。

## 彌補了什麼缺陷
- 列表推導式彌補了 `map`/`filter` + `lambda` 組合「可讀性差、嵌套 lambda 難懂」的缺陷（並在日後逐步取代它們）。
- 循環 GC 彌補了引用計數「循環引用永不釋放、記憶體洩漏」的根本缺陷。

## 程式範例

列表推導式（PEP 202）——前後對比：

```python
xs = [1, -2, 3, -4, 5]

# 2.0 之前：map + filter + lambda，嵌套 lambda 難懂
positives = map(lambda x: x*x, filter(lambda x: x > 0, xs))

# 2.0：列表推導式——描述「要什麼」，接近數學集合記法 {x² | x ∈ xs, x > 0}
positives = [x*x for x in xs if x > 0]   # [1, 9, 25]
```

循環垃圾回收（PEP 205）——引用計數的天敵：

```python
a = []
b = []
a.append(b)   # a 引用 b
b.append(a)   # b 引用 a —— 循環引用！
del a, b      # 引用計數不為零（互相引用），純引用計數永不回收
# 2.0 的循環偵測器會在週期性掃描中回收這塊記憶體
```

擴充指定與 Unicode：

```python
count = 0
count += 1        # PEP 203，取代 count = count + 1

s = u"中文"       # 2.0 的 unicode 型別：應對網際網路時代的多語系文字
```

## 相關條目

- [1994-Python-1-0問世](1994-Python-1-0問世.md)
- [2001-IPython與新式類別](2001-IPython與新式類別.md)
