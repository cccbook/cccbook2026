# 2025 - MCP 智慧代理: 模型上下文協議 (USB-C 式工具插槽) + ReAct 迴圈
# 對應本書: 2025-MCP智慧代理.md
# 公式: agent = LLM + 工具 + 迴圈; s_{t+1} = f(s_t, tool_result), a_t ~ π(s_t)
# 展示: 微型 MCP 主機 + 三個工具 (計算機/kv備忘/通訊錄) + ReAct 代理查「Alice 的貓幾歲」的多步任務
import json
import math

TOOLS = {}  # MCP 註冊表: 名字 -> (schema, 函式)


def tool(name, schema):
    def deco(fn):
        TOOLS[name] = (schema, fn)
        return fn
    return deco


@tool("calculator", {"expr": "數學式 (支援 + - * / sqrt)"})
def calc(expr: str):
    allowed = {k: getattr(math, k) for k in ("sqrt", "log", "sin", "cos", "pi")}
    return str(eval(expr, {"__builtins__": {}}, allowed))


MEMO = {}
CONTACTS = {"Alice": {"cat": "Mimi", "phone": "0911"}, "Bob": {"cat": None, "phone": "0922"}}
PETS = {"Mimi": {"age": 3}}


@tool("memo_write", {"key": "鍵", "value": "值"})
def memo_write(key: str, value: str):
    MEMO[key] = value
    return f"記住 {key}={value}"


@tool("memo_read", {"key": "鍵"})
def memo_read(key: str):
    return MEMO.get(key, "查無此鍵")


@tool("contacts", {"name": "人名"})
def contacts(name: str):
    return json.dumps(CONTACTS.get(name, {}), ensure_ascii=False)


@tool("pets", {"name": "寵物名"})
def pets(name: str):
    return json.dumps(PETS.get(name, {}), ensure_ascii=False)


def agent(task):
    """ReAct 迴圈的最小骨架: 想一步 -> 調一個工具 -> 看結果 -> 直到答案 (此處以規則路由代替 LLM)."""
    trace = [f"任務: {task}"]
    think = "要知道 Alice 的貓幾歲: 先查通訊錄找貓名, 再查寵物找年齡, 最後算成人類年齡(x7)."
    trace.append(f"思考: {think}")
    cat = json.loads(TOOLS["contacts"][1]("Alice"))["cat"]
    trace.append(f"調用 contacts(Alice) -> {cat} 的主人是 Alice")
    age = json.loads(TOOLS["pets"][1](cat))["age"]
    trace.append(f"調用 pets({cat}) -> {age} 歲")
    human = TOOLS["calculator"][1](f"{age}*7")
    trace.append(f"調用 calculator({age}*7) -> {human}")
    TOOLS["memo_write"][1]("alice_cat_human_age", human)
    trace.append("調用 memo_write 存檔")
    return trace, f"Alice 的貓 {cat} 今年 {age} 歲, 約等於人類 {human} 歲"


def main():
    print(f"MCP 註冊表 ({len(TOOLS)} 個工具, M×N 變 M+N): {sorted(TOOLS)}")
    trace, answer = agent("Alice 的貓幾歲 (換算人類年齡)?")
    for line in trace:
        print("  " + line)
    print("答案:", answer)
    print("備忘驗證:", TOOLS["memo_read"][1]("alice_cat_human_age"))
    print("結論: 工具標準化 + 迴圈 = 代理; 權限與審計是剎車 (見本文第四條線索)")


if __name__ == "__main__":
    main()
