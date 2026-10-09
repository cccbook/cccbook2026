# 1966 - ELIZA 對話系統 (Weizenbaum)
# 對應本書: 1966-ELIZA對話系統.md
# 核心: 樣板匹配 + 代名詞反射 (I->you, my->your), 無任何學習, 卻讓人覺得「被理解」
# 展示: DOCTOR 腳本縮影, 純 python (呼應: 智慧可以是符號操作, 不必是神經網路)
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
