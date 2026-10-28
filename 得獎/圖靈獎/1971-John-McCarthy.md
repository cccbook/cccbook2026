# 1971 John McCarthy —— 命名的天才：他發明了「人工智慧」這個詞

> 「誰替一門學科取了名字、發明了它的母語（LISP）、還提出了
> 分時系統？一人三案。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | John McCarthy (1927–2011) |
| 得獎理由 | AI 研究的重大影響：分時系統、LISP 語言、常識推理理論 |
| 關鍵詞 | LISP、分時系統、情境邏輯 |

## 前因

1955 年 McCarthy 為達特茅斯提案寫下 "Artificial Intelligence" 一詞
（1956 會議成真）。同時，當時一台電腦一天只服務一批人，
**昂貴的 CPU 大部分時間在等打字員**——資源浪費之謎。

## 線索與推理

### 案一：分時系統（1959 提案，MIT CTSS/1962）

McCarthy 提出：把 CPU 時間切片，輪流服務多個終端機使用者。
理論基礎是排程與公平性——**讓每個人以為自己獨佔整台機器**。
這是虛擬化思想的第一縷光（今日雲端運算直系祖先）。

### 案二：LISP（1958–1960）

目標：做 AI 需要一種「代數式表處理」語言。McCarthy 的關鍵洞見：

1. **用 S-expression 統一程式與資料**：

```
(cons 'a '(b c))   ; 資料
(+ 1 2)            ; 程式 —— 同一種記法
```

2. **函數即萬物**：直接把 Church 的 λ 演算搬進語言（參見
   科技史/λ演算 1958-LISP 案）。

3. **九頁論文定義整個語言**：`eval` 用 LISP 自身寫出（meta-circular
   evaluator）——程式語言第一次能**自我描述**。這引出日後的
   反射（reflection）與直譯器理論。

4. **垃圾回收**：記憶體自動管理自此誕生。

### 案三：情境邏輯（Situation Calculus, 1963/1969）

以一階邏輯表示動作與變化：

```
Holds(At(robot, home), do(walk(kitchen), s))
「在狀態 s 走到廚房後的狀態中，機器人在家」
```

以及非單調邏輯（circumscription, 1980）：常識推理必須容許
「新事實推翻舊結論」——古典邏輯做不到，AI 需要**可撤銷的推理**。

## 理論評析

McCarthy 的符號主義信條：「智慧的關鍵是**表示**（representation），
不是速度。」他與 Minsky 的分歧：Minsky 求諸心理學式架構（框架），
McCarthy 求諸數學邏輯。前者靈活、後者嚴格，AI 至今仍在兩岸之間。

## 後果

- LISP 主宰 AI 界三十年；Scheme、Clojure、JavaScript 的閉包、
  Python 的 list comprehension 皆有其血統。
- 分時系統直接啟發 UNIX（1983 案）與 ARPANET 終端文化（2004 案）。

## 關聯案件

→ [1969-Marvin-Minsky](1969-Marvin-Minsky.md)、[1958-LISP（λ演算史）](../科技史/λ演算/1958-LISP.md)、[1990-Fernando-Corbato](1990-Fernando-Corbato.md)
