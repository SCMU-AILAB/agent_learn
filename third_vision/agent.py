from tools import tool_explain,tool_list
import json
from memory.memory import memory
from llm import ask
import os


class Agent:
    def __init__(self):
        self.memory=memory(memory.get_history())

    def to_run(self,questions):
        message=[{"role":"system",
                  "content":"基于工具得到回答要简洁，直接给结论，不要展开推导过程。如果前一次调用工具的失败，但用户依旧提出使用gai gong j。"}
            ]+self.memory.read_history()+[{"role":"user","content":questions}]

        epochs=8
        count=0

        for i in range(epochs):
            count+=1
            answers=ask(message,tools=tool_explain)
            message.append(answers)

            apply_list=answers.get("tool_calls") or []

            if apply_list==[]:
                print(f"运行{count}次")
                self.memory.save_history(message[1:])
                return answers.get("content")

            for apply in apply_list:
                print(" ->模型申请调用：",apply["function"]["name"])
                name=apply["function"]["name"]
                arges=json.loads(apply["function"]["arguments"] or "{}")

                if name in tool_list.keys():
                    conl=tool_list[name](**arges)
                else:
                    message.append({"role": "tool", "tool_call_id": apply["id"], "content": "警告:工具不存在"})
                    self.memory.save_history(message[1:])
                    return "警告:模型申请的工具不存在!!!"

                message.append(
                    {
                        "role":"tool",
                        "tool_call_id":apply["id"],
                        "content":str(conl)
                    }
                )
        self.memory.save_history(message[1:])
        return "轮次已用完"
                    