# 1975-Minsky框架理論

## 案件摘要

1975 年，Marvin Minsky 在 MIT AI Memo 306《A Framework for Representing Knowledge》中提出「框架」（frame）理論，企圖解決常識知識表示的懸案。邏輯式表示法在處理「典型情境」時屢屢碰壁，Minsky 主張知識應組織成一個個帶有槽位（slot）與預設值（default）的結構。這份文件後來收錄於《The Psychology of Computer Vision》論文集，成為知識表示法的轉捩點。本案的破案時刻在於：用「結構 + 預設 + 填入」取代「原子 + 邏輯連接詞」，讓機器第一次能「預期」世界。

## 前因 -- 為什麼會有這個案子

- 一階邏輯（predicate logic）只能表達「為真的事實」，無法優雅地表達「預設」（default）與「典型情境」——「鳥會飛，除非是企鵝」這種常識讓邏輯學家頭痛。
- 視覺理解研究發現：人看房間時並非從零建構，而是「召喚」一個房間的模板再檢查細節；語言理解同樣依賴情境預期。
- Erving Goffman 1974 年《Frame Analysis》從社會學角度指出人用「框架」詮釋情境；Schank 的概念依賴理論（Conceptual Dependency）也主張意義背後有深層結構。
- Minsky 在 MIT AI Lab 長期研究常識推理，深知機器人可以下棋，卻不懂「走進餐廳會發生什麼」。
- 當時 AI 界需要一種能同時承載視覺、語言、計劃的統一知識結構。

## 線索與推理 -- 數學式、程式、理論

### 框架的表示法

一個框架是「名稱 + 槽位集合」：每個 slot 可填入 filler（具體值）、default（預設值）或另一個框架的參照。形式上可寫成：

$$
F = \langle \text{name}, \{(s_1, v_1), (s_2, v_2), \ldots\} \rangle, \quad v_i \in \{\text{filler}, \text{default}, F'\}
$$

查詢槽位時的取值規則：先看實例是否填入，否則沿繼承鏈上溯取預設：

$$
v(s) = \begin{cases} \text{filler}(s, F) & \text{若有填入} \\ v_{\text{parent}}(s) & \text{否則遞迴上溯} \\ \text{default}(s, F_{\text{root}}) & \text{抵達根類別} \end{cases}
$$

### 餐廳腳本與航班框架

Minsky 舉例：進入餐廳的框架有 slot「入座、點菜、用餐、付帳」，每個 slot 有典型預設（付帳通常是「付現金或刷卡」）。飛機航班框架則示範了繼承：`航班` 有 slot「出發地、目的地、起飛時間」，`國際航班` 繼承並附加新 slot「護照檢查」。

### 框架與物件導向的同構

框架與物件導向程式設計（OOP）幾乎同構，但哲學層次不同——Simula 1967 是 OOP 的程式實作，frame 是知識表示（KR）層次的主張：

| 框架 | OOP |
|------|-----|
| frame（框架） | class（類別） |
| slot（槽位） | attribute（屬性） |
| default（預設值） | default value |
| 實例化填入 filler | instance + constructor |
| 框架附加 | inheritance / composition |

### 填充-匹配的推理流程

理解 = 選一個候選框架，把觀察到的線索填入 slot，不匹配處用 default 補齊並標記為「待檢查」。這是一種「預期驅動」的自上而下推理，與資料驅動的自下而上匹配互補。

### Python 實作 mini 框架系統

```python
class Frame:
    def __init__(self, name, parent=None, slots=None):
        self.name = name
        self.parent = parent
        self.slots = slots or {}   # slot -> {"default": v} 或 {"value": v}

    def set(self, slot, value):
        self.slots[slot] = {"value": value}

    def get(self, slot):
        f = self
        while f is not None:
            entry = f.slots.get(slot)
            if entry:
                if "value" in entry:          # 優先取填入的 filler
                    return entry["value"]
                if "default" in entry:        # 其次取預設值
                    return entry["default"]
            f = f.parent                       # 沿繼承鏈上溯
        return None

    def instantiate(self, name, fillers):
        child = Frame(name, parent=self)
        for slot, value in fillers.items():
            child.set(slot, value)
        return child


# 建構「餐廳腳本」框架
restaurant = Frame("Restaurant", slots={
    "sit_down":  {"default": "找空位入座"},
    "order":     {"default": "看菜單點菜"},
    "eat":       {"default": "用餐"},
    "pay":       {"default": "付現金或刷卡"},
})

# 飛機航班框架與繼承
flight = Frame("Flight", slots={
    "origin":    {"default": "本地機場"},
    "dest":      {"default": "未知"},
    "boarding":  {"default": "憑登機證登機"},
})
intl_flight = Frame("IntlFlight", parent=flight, slots={
    "passport":  {"default": "護照檢查"},   # 附加新 slot
})

# 實例化：填入 filler
dinner = restaurant.instantiate("Dinner-2025-01", {"pay": "用 App 付款"})
trip = intl_flight.instantiate("Trip-TPE-NRT", {"dest": "東京成田"})

print(dinner.get("pay"))      # 填入值覆蓋預設 -> 用 App 付款
print(dinner.get("order"))    # 無填入，取預設 -> 看菜單點菜
print(trip.get("dest"))       # 填入值 -> 東京成田
print(trip.get("boarding"))   # 從父類 Flight 繼承 -> 憑登機證登機
print(trip.get("passport"))   # 自己的預設 -> 護照檢查
```

## 結案 -- 後果與影響

- 框架成為知識表示法的標準範式，衍生出 KL-ONE（1983）與日後的描述邏輯（description logic）。
- 為物件導向設計提供哲學先聲：frame = class 的同構讓 KR 社群與程式語言社群開始對話。
- 腳本理論（Schank 與 Abelson 1977《Scripts, Plans, Goals, and Understanding》）以框架為理論基礎，推動故事理解研究。
- 缺陷浮現：預設推理會產生矛盾（「企鵝是鳥但不會飛」破壞繼承），催生 1980 年代的非單調邏輯（non-monotonic logic）。
- 「預期驅動理解」的思想延續到日後的統計語言模型：現代 LM 同樣在做「召喚典型情境再填空」。

## 關鍵人物與文獻

- Marvin Minsky (1975). A Framework for Representing Knowledge. MIT AI Memo 306；收錄於 P. Winston (ed.), The Psychology of Computer Vision. McGraw-Hill, 1975, pp. 211-277.
- Marvin Minsky (1968). Semantic Information Processing. MIT Press.
- Erving Goffman (1974). Frame Analysis: An Essay on the Organization of Experience. Harvard University Press.
- Roger Schank (1972). Conceptual Dependency: A Theory of Natural Language Understanding. Cognitive Psychology 3(4), 552-631.
- Roger Schank & Robert Abelson (1977). Scripts, Plans, Goals, and Understanding. Lawrence Erlbaum.
- Ronald Brachman & James Schmolze (1985). An Overview of the KL-ONE Knowledge Representation System. Cognitive Science 9(2), 171-216.
