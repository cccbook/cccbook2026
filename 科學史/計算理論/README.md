# 計算理論史 -- AI 偵探風格

以「推理探案」的方式，追查計算理論從 Hilbert 綱領到今日計算複雜度理論的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個電腦科學？

## 案件卷宗（歷史年表）

### 序幕：數學基礎的危機（1900–1930）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1900 | Hilbert 提出 23 個數學問題（含判定問題） | [1900-Hilbert23問題.md](1900-Hilbert23問題.md) |
| 1913 | Löwenheim–Skolem 定理與一階邏輯 | [1913-LowenheimSkolem定理.md](1913-LowenheimSkolem定理.md) |
| 1931 | Gödel 不完備定理震撼數學基礎 | [1931-Godel不完備定理.md](1931-Godel不完備定理.md) |
| 1933 | Church–Kleene 提出 λ 可定義性 | [1933-Lambda可定義性.md](1933-Lambda可定義性.md) |

### 可計算性的誕生（1936–1943）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1936 | Turing 提出圖靈機與停機問題不可判定 | [1936-Turing機與停機問題.md](1936-Turing機與停機問題.md) |
| 1936 | Kleene 提出部分遞迴函數（μ-遞迴函數） | [1936-Mu遞迴函數.md](1936-Mu遞迴函數.md) |
| 1937 | Post 提出郵務對應問題與 Post 系統 | [1937-Post系統.md](1937-Post系統.md) |
| 1938 | Church–Turing 命題正式確立 | [1938-ChurchTuring命題.md](1938-ChurchTuring命題.md) |
| 1943 | Post 正式提出 Post 對應問題（PCP）不可判定 | [1943-Post對應問題.md](1943-Post對應問題.md) |

### 遞迴論與自動機（1940s–1950s）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1936–1956 | 有限狀態機（FSM）與 Kleene 定理（正則語言 = FSM） | [1936-Kleene定理與正則語言.md](1936-Kleene定理與正則語言.md) |
| 1944 | Post 提出不可解度（Turing degree） | [1944-Post不可解度.md](1944-Post不可解度.md) |
| 1950 | Rice 定理：所有非平凡語義性質皆不可判定 | [1950-Rice定理.md](1950-Rice定理.md) |
| 1956 | Chomsky 階層：四類文法與四類自動機 | [1956-Chomsky階層.md](1956-Chomsky階層.md) |
| 1959 | Kleene 的正則表達式定理正式發表 | [1959-正則表達式.md](1959-正則表達式.md) |

### 計算複雜度的誕生（1960s–1970s）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1956 | Gödel 的信件：首次想到「複雜度」問題 | [1956-Godel的信件.md](1956-Godel的信件.md) |
| 1965 | Cobham–Edmonds 定義多項式時間 P | [1965-CobhamEdmonds多項式時間.md](1965-CobhamEdmonds多項式時間.md) |
| 1965 | Hartmanis–Stearns 建立時間階層定理 | [1965-HartmanisStearns時間階層.md](1965-HartmanisStearns時間階層.md) |
| 1967 | Cook 提出可滿足性與 NP-complete（SAT） | [1967-Cook定理.md](1967-Cook定理.md) |
| 1971 | Cook–Levin 定理：SAT 是 NP-complete | [1971-CookLevin定理.md](1971-CookLevin定理.md) |
| 1971 | Karp 的 21 個 NP-complete 問題 | [1971-Karp21問題.md](1971-Karp21問題.md) |
| 1975 | Levin 獨立提出 NP-complete（蘇聯） | [1975-LevinNP完備.md](1975-LevinNP完備.md) |

### 現代計算複雜度（1980s–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1975 | Baker–Gill–Solovay：相對化世界中的 P vs NP | [1975-相對化世界.md](1975-相對化世界.md) |
| 1979 | Cook–Karp 綱領下 Garey–Johnson 出版 NP-hardness 聖經 | [1979-GareyJohnson聖經.md](1979-GareyJohnson聖經.md) |
| 1985 | Babai 提出互動式證明系統（IP） | [1985-互動式證明系統.md](1985-互動式證明系統.md) |
| 1990 | PCP 定理：NP 擁有可驗證的機率式證明 | [1990-PCP定理.md](1990-PCP定理.md) |
| 2000 | Clay 數學研究所提出 P vs NP 千禧年大獎 | [2000-PvsNP千禧年大獎.md](2000-PvsNP千禧年大獎.md) |
| 2002 | Agrawal–Kayal–Saxena 提出 AKS 質數檢驗（P 中的質數測試） | [2002-AKS質數檢驗.md](2002-AKS質數檢驗.md) |
| 2019 | 電路複雜度與 P vs NP 的最新進展（Mulmuley 幾何複雜度理論） | [2019-幾何複雜度理論.md](2019-幾何複雜度理論.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1900 | David Hilbert | 23 問題、判定問題 |
| 1931 | Kurt Gödel | 不完備定理 |
| 1933 | Church / Kleene | λ 可定義性 |
| 1936 | Alan Turing | 圖靈機、停機問題 |
| 1936 | Stephen Kleene | μ-遞迴函數 |
| 1937 | Emil Post | Post 系統、PCP |
| 1944 | Emil Post | 不可解度 |
| 1950 | Henry Rice | Rice 定理 |
| 1956 | Noam Chomsky | Chomsky 階層 |
| 1965 | Cobham / Edmonds | 多項式時間 P |
| 1965 | Hartmanis / Stearns | 時間階層定理 |
| 1971 | Stephen Cook / Levin | Cook–Levin 定理 |
| 1971 | Richard Karp | 21 個 NP-complete |
| 1985 | László Babai | 互動式證明系統 |
| 1990 | PCP 學派 | PCP 定理 |
| 2002 | Agrawal / Kayal / Saxena | AKS 質數檢驗 |
