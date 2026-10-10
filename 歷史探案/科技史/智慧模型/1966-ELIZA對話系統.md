# 1966 - ELIZA 對話系統

## 案件摘要

1966 年，MIT 的 Joseph Weizenbaum 發表了 ELIZA——史上第一個聊天機器人。它的全部「智慧」只是模式比對加範本替換：把使用者說的話套進預設的心理治療回應範本。最著名的 DOCTOR 腳本扮演羅傑斯學派心理治療師：

$$\text{回應} = \text{替換}\big(\text{範本}(\text{輸入})\big)，\quad \text{智慧感} \gg \text{實際智慧}$$

Weizenbaum 的震驚在於：**使用者明知程式只是字串替換，卻依然對它傾訴內心**。這個現象被稱為「Eliza 效應」——人類把智慧投射到最粗糙的語言機器上。這既是 NLP 的起點，也是一桩關於人類認知弱點的懸案。

## 前因 -- 為什麼會有這個案子

- 圖靈 1950 年的模仿遊戲（見「科學與歷史/人工智慧/」下圖靈測試相關檔案）提出：機器若能在對話中騙過人類，即可視為有智慧。ELIZA 是第一個認真嘗試「騙過人類」的程式。
- 1960 年代 NLP 的主流是機器翻譯與語法解析（Chomsky 變換生成語法），工程浩大、進展緩慢；1966 年 ALPAC 報告更判機器翻譯「死刑」，經費凍結。
- Weizenbaum 的動機原本是**批判性**的：他想展示「自然語言理解」有多淺薄——一個只做表面模式比對的程式就能讓人覺得它懂。
- SLIP 語言（Weizenbaum 自創的 list-processing 語言）提供了字串比對與替換的實作基礎。
- 1956 年 Newell 與 Simon 的 GPS 主張通用推理，ELIZA 反其道而行：完全不推理，只反應。
- 分時系統（CTSS）剛在 MIT 出現，使用者第一次能透過打字機終端與電腦「對話」——舞台已備好。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：模式比對 + 範本替換

ELIZA 的核心機制只有兩步。對每句輸入，依序檢查一組「關鍵字 + 分解範本」（decomposition pattern），命中後套用「重組規則」（reassembly rule）：

$$(\text{keyword},\ \text{pattern},\ \text{template})：\quad \text{"I am } X\text{"} \Rightarrow \text{"How long have you been } X\text{?"}$$

規則以優先序排列，關鍵字越具體優先權越高；無命中時使用萬用回應（如 "Please go on."）。

### 第二條線索：一個 Python 縮影

ELIZA 的本質可以用十餘行 Python 重現（原版為 SLIP/LISP，此為闡明用縮影）：

```python
import re
rules = [
    (r'.*I am (sad|depressed|unhappy).*', 'Why do you think you are {0}?'),
    (r'.*I need (.*)', 'What would it mean to you if you got {0}?'),
    (r'.*my (mother|father|family)(.*)', 'Tell me more about your family.'),
    (r'.*you (.*)', 'Why do you say I {0}?'),
]
def eliza(text):
    for pat, tmpl in rules:
        m = re.match(pat, text, re.I)
        if m:
            return tmpl.format(*m.groups())
    return 'Please go on.'
print(eliza('I am sad because of my job'))   # Why do you think you are sad?
print(eliza('I need someone to talk to'))    # What would it mean to you if you got someone to talk to?
print(eliza('You never listen to me'))       # Why do you say I never listen to me?
```

輸出如註解所示——三句話，零理解，卻像極了一位治療師。注意第三條規則甚至把 "you X" 鏡射回 "Why do you say I X"，這正是 ELIZA 最像人的把戲。

### 第三條線索：DOCTOR 腳本的心理學巧思

Weizenbaum 選擇羅傑斯學派（client-centered therapy）絕非偶然：

| 羅傑斯治療師的特徵 | 對 ELIZA 的工程意義 |
|---|---|
| 以反問回應，不給建議 | 範本只需回拋使用者的話 |
| 不主動引導話題 | 不需對話狀態與長期記憶 |
| 接納而非質疑 | 無需語意一致性檢查 |

換言之，**治療師是唯一一種「淺薄反應即合理」的對話者**——DOCTOR 腳本把領域選在了理解門檻最低處。這與 DENDRAL 的策略異曲同工（見「1965-DENDRAL專家系統.md」）：選窄而淺的場景，避開通用理解的深水區。

### 第四條線索：Eliza 效應——投射的認知機制

Weizenbaum 觀察到：秘書們明知 ELIZA 是程式，仍要求「與它私下談話」；他的精神科同事甚至建議讓它廣泛應用。效應的根源在於：

- 人類預設以「擬人濾鏡」解讀任何流暢輸出的語言信號（語言 = 心智的強推斷）。
- 對話是輪替的，人類會主動補全語意空隙——理解的工作其實由**使用者自己**完成。
- 這預示了現代大型語言模型的同一課題：流暢性與理解、擬人化與信任的界線（見「科學與歷史/人工智慧/」下 LLM 相關檔案）。

## 結案 -- 後果與影響

- ELIZA 成為 NLP 與人機互動（HCI）的起點之一：模式比對聊天機器的祖先一直延續到今天的客服機器人。
- Weizenbaum 本人卻被效應嚇到轉向批判陣營，1976 年出版 *Computer Power and Human Reason*，警告人類不應把道德判斷交給機器——發明者成為最著名的反對者。
- 「Eliza 效應」成為 AI 伦理與 HCI 的標準術語，如今用於描述人類對 LLM 的過度信任。
- 它證明了對話介面的心理威力，為後來的對話式 AI（見「科學與歷史/人工智慧/」與「科學與歷史/計算語言學/」下對應檔案）鋪路。
- 伏筆：ELIZA 的「智慧」是錯覺，但它提出了一個直達本書核心的問題——**承載智能的到底是模型本身，還是使用者與模型共同構成的系統？** 半個世紀後，當語言模型真的能推理時，這個問題將以新的形式重演。
- 同時期的連結派正走向寒冬（見「1969-MinskyPapert批判.md」）；符號派的 ELIZA 與 DENDRAL 卻風光無兩——但兩者的「淺薄」都將被日後更深的方法翻案。

## 關鍵人物與文獻

- Joseph Weizenbaum —— ELIZA 設計者，後期 AI 批判者
- Weizenbaum, "ELIZA — A computer program for the study of natural language communication between man and machine", *CACM*, 1966
- Weizenbaum, *Computer Power and Human Reason*, 1976
- Rogers, *Client-Centered Therapy*, 1951（DOCTOR 腳本的模板來源）
- Turing, "Computing Machinery and Intelligence", 1950（對話智慧的哲學源頭）
- 相關案件：1965-DENDRAL專家系統.md、1969-MinskyPapert批判.md、1980-XCON專家系統黃金時代.md

## 補充 -- 程式實作（python，無需學習的樣板匹配）

本案 DOCTOR 腳本的核心機制——樣板匹配＋代名詞反射——最小可執行版本，見 `_code/1966-ELIZA.py`（已實測可跑）：

```python
# 1966 - ELIZA 對話系統 (Weizenbaum)
# 核心: 樣板匹配 + 代名詞反射 (I->you, my->your), 無任何學習
import re

REFLECT = {
    "i": "you", "me": "you", "my": "your", "mine": "yours",
    "you": "I", "your": "my", "yours": "mine", "am": "are",
}
RULES = [
    (r"i need (.*)", ["Why do you need {0}?", "Would {0} really help you?"]),
    (r"i feel (.*)", ["How long have you felt {0}?", "Do you often feel {0}?"]),
    (r"i am (.*)", ["How long have you been {0}?", "Why do you say you are {0}?"]),
    (r"i remember (.*)", ["Why do you remember {0} just now?", "What does {0} remind you of?"]),
    (r"(.*) mother (.*)", ["Tell me more about your mother.", "How does your mother make you feel?"]),
    (r"(.*) father (.*)", ["Tell me more about your father."]),
    (r"yes", ["You seem quite sure.", "I see."]),
    (r"no", ["Why not?", "Are you saying no just to be negative?"]),
    (r"(.*)", ["Please go on.", "Can you elaborate on that?", "How does that make you feel?"]),
]


def reflect(text):
    return " ".join(REFLECT.get(w.lower(), w) for w in re.findall(r"[A-Za-z']+", text))


def eliza_reply(sentence, turn=0):
    s = sentence.strip().rstrip(".!?").lower()
    for pat, responses in RULES:
        m = re.fullmatch(pat, s)
        if m:
            resp = responses[turn % len(responses)]
            groups = [reflect(g) for g in m.groups()]
            return resp.format(*groups) if groups else resp
    return "..."


def main():
    demo = ["I need help", "I feel sad", "I remember my childhood",
            "My mother loves me", "yes", "I am tired of homework"]
    print("ELIZA (DOCTOR 腳本縮影) -- 樣板匹配 + 代名詞反射, 無學習:")
    for i, s in enumerate(demo):
        print(f"  YOU  : {s}")
        print(f"  ELIZA: {eliza_reply(s, i)}")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/1966-ELIZA.py`）：

```
ELIZA (DOCTOR 腳本縮影) -- 樣板匹配 + 代名詞反射, 無學習:
  YOU  : I need help
  ELIZA: Why do you need help?
  YOU  : I feel sad
  ELIZA: Do you often feel sad?
  YOU  : I remember my childhood
  ELIZA: Why do you remember your childhood just now?
  YOU  : My mother loves me
  ELIZA: How does your mother make you feel?
  YOU  : yes
  ELIZA: You seem quite sure.
  YOU  : I am tired of homework
  ELIZA: Why do you say you are tired of homework?
```

程式解說：全案智慧只來自兩招——`RULES` 的正則樣板把輸入拆出關鍵片語，`reflect` 把片語中的人稱代名詞翻轉（`my → your`、`I → you`）再塞回問句，偽裝成「理解」。注意第三句：`my childhood` 被翻成 `your childhood`，正是 Weizenbaum 論文點名的反射機制。不到 60 行、零參數、零訓練，卻足以讓 1966 年的受試者傾訴心事——此即本案論旨： **「顯得理解」與「真的理解」在行為層面可以分離** ，Searle 中文房間與圖靈測試之辯的活體證據。
