# 2011 - Siri 語音助理: 意圖分類 + 槽位填空 (intent-slot 範式)
# 對應本書: 2011-Siri語音助理.md
# 管線: 文本 -> TF-IDF -> 意圖分類 -> 正則槽位; 展示此範式的天花板 (GPU 種子也在其中)
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

COMMANDS = [
    ("call mom tomorrow morning", "打電話", {"對象": "mom", "時間": "tomorrow morning"}),
    ("call dad tonight", "打電話", {"對象": "dad", "時間": "tonight"}),
    ("text mom I am late", "傳訊息", {"對象": "mom", "內容": "I am late"}),
    ("text dad call me back", "傳訊息", {"對象": "dad", "內容": "call me back"}),
    ("set alarm for 7 am", "設鬧鐘", {"時間": "7 am"}),
    ("set alarm for 8 pm", "設鬧鐘", {"時間": "8 pm"}),
    ("play some jazz music", "放音樂", {"類型": "jazz"}),
    ("play rock music loudly", "放音樂", {"類型": "rock"}),
    ("what is the weather today", "查天氣", {"時間": "today"}),
    ("what is the weather tomorrow", "查天氣", {"時間": "tomorrow"}),
    ("remind me to buy milk", "設提醒", {"事項": "buy milk"}),
    ("remind me to call mom", "設提醒", {"事項": "call mom"}),
]
SLOT_RES = {
    "對象": r"(mom|dad)",
    "時間": r"(tomorrow morning|tonight|7 am|8 pm|today|tomorrow)",
    "類型": r"(jazz|rock)",
    "內容": r"(?:text \w+ )(.+)",
    "事項": r"(?:remind me to )(.+)",
}


def fill_slots(text):
    return {k: (m.group(1) if (m := re.search(p, text)) else None)
            for k, p in SLOT_RES.items()}


def main():
    texts = [c[0] for c in COMMANDS]
    intents = [c[1] for c in COMMANDS]
    clf = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=500))
    clf.fit(texts, intents)
    tests = ["call mom tonight", "play jazz music", "set alarm for 7 am",
             "what is the weather today", "Call Dad Tomorrow Morning", "remind me to buy milk"]
    print("意圖分類 + 槽位填空 (intent-slot 範式, 2011-2021 的 Siri 心臟):")
    for t in tests:
        intent = clf.predict([t])[0]
        slots = {k: v for k, v in fill_slots(t.lower()).items() if v}
        print(f"  '{t}' -> 意圖={intent} 槽位={slots}")
    print(f"訓練集回測準確率={clf.score(texts, intents):.2f} (封閉世界滿分 -- 一出新說法即崩)")
    print("結論: 意圖×槽位的窮舉是一座監獄 -- LLM 用『一句話生成』越獄 (見 2022-ChatGPT與RLHF.md)")


if __name__ == "__main__":
    main()
