from llm import ask
from memory import read_history,save_history,history
import json
import os

def to_run(questions,tool_explain,tool_list):
    message=[{"role": "system", "content": "回答要简洁，直接给结论，不要展开推导过程。"}
    ]+read_history()+[{"role":"user","content":questions}]

    epochs=8
    count=0

    for i in range(epochs):
        count+=1
        answers = ask(message,tools=tool_explain)
        message.append(answers)

        apply_list=answers.get("tool_calls") or []

        if apply_list==[]:
            print(f"运行{count}次")
            save_history(message=message[1:])
            return answers.get("content")

        for apply in apply_list:
            print("  → 模型申请调用:", apply["function"]["name"])     # ← 加这行
            name = apply["function"]["name"]
            arges=json.loads(apply["function"]["arguments"] or "{}")

            if name in tool_list.keys():
                conl=tool_list[name](**arges)
            else:
                return "警告:模型申请的工具不存在!!!"

            message.append({
                "role": "tool",
                "tool_call_id": apply["id"],
                "content": str(conl),
            })#append每次只能写入一个{}

    return "轮次已用完"