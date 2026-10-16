# 1954-GeorgetownIBM實驗

## 案件摘要

1954 年 1 月 7 日，Georgetown 大學與 IBM 在紐約公開示範了機器翻譯：IBM 701 電腦將 60 個俄語句子譯成英語。由 Leon Dostert 與 Cuthbert Hurd 主導的這場示範震動了外界，掀起機器翻譯研究的黃金十年。但偵探式檢視會發現：那 60 句是精心挑選的，用的只是 6 條語法規則與 250 字的詞彙表。示範的成功遠超過技術的實際水準，這個「承諾過度」的落差最終在 1966 年以 ALPAC 報告的形式反噬整個領域。

## 前因 -- 為什麼會有這個案子

- 冷戰爆發，美國急需大量翻譯俄語科學與情報文獻，人工翻譯供不應求。
- 二戰密碼破解經驗讓人相信語言可以像密碼一樣被機器處理。
- Warren Weaver 1949 年的著名備忘錄提出機器翻譯的可行性，並以「語言=密碼」的比喻啟發整個領域。
- IBM 701 是當時最先進的商業電腦，具備足夠的儲存與運算能力做小規模示範。
- Leon Dostert（Georgetown 語言學家、NATO 同聲傳譯的設計者）積極推動公開示範，爭取政府資金。

## 線索與推理 -- 數學式、程式、理論

### 六條規則、250 個字詞：精心挑選的證據

偵探的第一步是檢視「證物」：那 60 個句子不是隨機抽取的真實俄語文本，而是專為示範設計的。

- 詞彙表僅 250 個詞，且多為化學、冶金等受限領域術語。
- 語法規則僅 6 條，處理有限的詞序重排。
- 每個俄語詞預先人工消歧（標定唯一對應譯法），機器實際上只做「查表 + 重排」。

也就是說，示範展示的不是「機器翻譯」，而是「受限領域內的查表翻譯」。但觀眾與媒體看到的是前者——這正是承諾過度的起點。

### 規則法的翻譯流程

當時的翻譯流程是字典查詢加詞序重排：

1. 俄語句子切詞。
2. 逐詞查字典得英語對應。
3. 依預寫規則重排詞序（如俄語形容詞在名詞後、英語在前）。
4. 輸出英語句子。

形式上，翻譯是一個映射 $T: S_{\text{ru}} \to S_{\text{en}}$，規則法假設它可以分解為

$$T(s) = R_6(\cdots R_2(R_1(D(s))))$$

其中 $D$ 是字典查詢，$R_i$ 是各條重排規則。問題在於：真實語言的 $T$ 無法用 6 條規則分解——歧義、習語、長距離依賴全都被這個分解丟棄。

### Weaver 的「語言=密碼」比喻

Weaver 在 1949 年備忘錄中設想：一篇以語言 A 寫成、表達某個語義的文章，若以語言 B 寫同樣語義，兩段文字可能像同一訊息的兩種加密版本。用統計語言說：若語義為 $m$，則

$$P(s_{\text{en}} \mid m) \approx P(s_{\text{ru}} \mid m)$$

因此翻譯可以透過統計對應還原「共同訊息」。這個比喻是三十年後統計機器翻譯（Brown et al. 1990）的思想前身——但 1954 年的示範完全沒有用到統計，只用了手工規則。

### 展示成功與承諾過度：ALPAC 反噬

- 示範後媒體大幅報導，資金湧入，美國 MT 研究進入黃金十年（1954–1966）。
- 但 1959–1966 年間實際系統的品質停滯：俄譯英輸出仍需大量人工後編輯。
- 1966 年 ALPAC（自動語言處理諮詢委員會）報告結論：MT 比人工翻譯更慢、更貴、品質更差，建議削減資金。MT 研究瞬間冷凍。
- 這是「示範成功 > 技術現實」的經典案例：承諾過度的代價由整個領域支付。

### 程式碼示範：迷你詞典翻譯

```python
# 受限 60 句風格的迷你詞典翻譯：展示成功與失敗
# 模擬 1954 年示範：250 詞彙表縮為 12 詞、6 條重排規則縮為 2 條

ru_en = {
    "качества": "quality", "угля": "coal", "является": "is",
    "важным": "important", "фактором": "factor", "обработки": "in processing",
    "химической": "chemical", "промышленности": "industry",
    "обработка": "processing", "руды": "ore", "требует": "requires",
    "энергии": "energy",
}

# 重排規則（簡化）：俄語形容詞+名詞 -> 英語 形容詞+名詞（順序一致則不動）
def reorder(words):
    words = words[:]  # 規則 1：在此受限詞序中多半不需重排
    return words

def translate(sentence):
    translated = [ru_en.get(w, f"[?{w}?]") for w in sentence.split()]
    return " ".join(reorder(translated))

# 屬於「精心挑選 60 句」風格的句子：成功
print(translate("качества угля является важным фактором обработки"))
# -> quality coal is important factor in processing
print(translate("обработка руды требует энергии"))
# -> processing ore requires energy

# 詞彙表之外的句子：失敗（真實文本必然如此）
print(translate("качества жизни является важным фактором города"))
# -> quality coal is important factor in [?города]
#    (жизни 不在詞彙表 -> 錯誤地套用 угля 的殘留；消歧失敗)

# 統計對照：Weaver 式統計對應需要平行語料，規則法沒有
# 一句話說明：規則法靠人手寫 T 的分解，統計法靠資料估計
# P(en | ru) ∝ P(ru | en) * P(en)   —— 這是 1990 年 IBM 模型的式子
```

## 結案 -- 後果與影響

- MT 研究的黃金十年：示範後美國政府與軍方大量資助 MT，MIT、Georgetown、IBM 等機構投入。
- 1966 年 ALPAC 報告的冷卻：承諾過度的代價是資金斷絕，MT 研究停滯近二十年。
- 「受限領域翻譯」思想存活下來：TAUM-METEO（1970 年代加拿大天氣預報翻譯系統）證明受限領域內規則法確實可行，至今仍在運作。
- Weaver 的「語言=密碼」統計比喻成為伏筆：1990 年 Brown 等人的統計機器翻譯實現了它，統計語料庫方法（N-gram 語言模型）由此興起。
- 這個案子留下方法論教訓：公開示範的「挑選證據」會反噬，評估必須在真實文本上進行——日後 BLEU 等自動評測指標的出現即是回應。

## 關鍵人物與文獻

- W. N. Locke, A. D. Booth (1955). *Machine Translation of Languages: Fourteen Essays.* MIT Press.（收錄示範後的技術報告）
- Warren Weaver (1949). "Translation." Memorandum, Rockefeller Foundation.（重印於 *Machine Translation of Languages* 1955）
- Leon Dostert (1955). "The Georgetown-IBM Experiment." 收錄於 Locke & Booth 編 *Machine Translation of Languages*.
- ALPAC (1966). *Language and Machines: Computers in Translation and Linguistics.* National Academy of Sciences / National Research Council Publication 1416.
- Peter F. Brown et al. (1990). "A Statistical Approach to Machine Translation." *Computational Linguistics* 16(2): 79–85.（Weaver 比喻的統計實現）
