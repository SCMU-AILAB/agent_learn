# third_vision/agent.py
"""Agent 主循环：组消息 → 问模型 → 执行它申请的工具调用，并把结果写回历史."""

import json

from config import MAX_ITERATIONS, MAX_TOOL_CALLS, MAX_SAME_CALL_REPEATS
from llm import ask
from memory.memory import memory
from tools import tr


class Agent:
    def __init__(self):
        self.memory = memory(memory.get_history())

    @staticmethod
    def call_key(name: str, args: dict) -> str:
        """一次调用以函数名和参数构成字符串返回当键：同名同参数->才为同一个键."""
        return f"{name}:{json.dumps(args, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}"

    def to_run(self, questions) -> str | None:
        message = (
            [
                {
                    "role": "system",
                    "content": (
                        "基于工具来回答，回答要简洁，直接给结论，不要展开推导过程。"
                        "如果上一次调用工具失败了，用户又提出同样的要求，可以再试一次。"
                        "如果这一轮的工具调用次数已经用完：不要自己计算、不要编造工具结果，"
                        "直接说明「这一项因为本轮工具调用次数用完，我没有拿到」，"
                        "并讲清用已有的结果能得出什么。"
                    )                
                }
            ]
            + self.memory.read_history()
            + [{"role": "user", "content": questions}]
        )

        calls_seen = {}

        epochs = MAX_ITERATIONS
        tools_count = 0
        count = 0

        for i in range(epochs):
            count += 1
            answers = ask(message, tools=tr.schemas)
            message.append(answers)

            apply_list = answers.get("tool_calls") or []

            if apply_list == []:
                print(f"运行{count}次")
                self.memory.save_history(message[1:])
                return answers.get("content")

            for apply in apply_list:
                tools_count += 1
                print(" ->模型申请调用：", apply["function"]["name"])
                name = apply["function"]["name"]
                args = json.loads(apply["function"]["arguments"] or "{}")

                key = self.call_key(name, args)

                if name in tr.registered_tools:
                    if tools_count > MAX_TOOL_CALLS:
                        message.append(
                            {"role": "tool", "tool_call_id": apply["id"], 
                             "content":(
                                  f"工具调用预算已用完（上限 {MAX_TOOL_CALLS} 次），本次未执行,"
                                  "工具没有损坏，只是这一轮不能再调；请基于已有结果回答。"
                                )}
                        )
                    else:
                        conl = tr.call(name, args)
                        _, _, tp = tr.registered_tools[name]
                        if (not tp.read_only) and calls_seen[key] > MAX_SAME_CALL_REPEATS:
                            message.append(
                                {"role": "tool", "tool_call_id": apply["id"],
                                "content": f"这个调用重复已达上限（{MAX_SAME_CALL_REPEATS} 次），"
                                            "本次不再执行；请换个办法，或基于已有结果回答。"}
                        )
                        calls_seen[key] = calls_seen.get(key,0) + 1
                        message.append(
                            {"role": "tool", "tool_call_id": apply["id"], "content": str(conl)}
                        )
                else:
                    message.append(
                        {
                            "role": "tool",
                            "tool_call_id": apply["id"],
                            "content": "警告:工具不存在",
                        }
                    )
                    self.memory.save_history(message[1:])
                    return "警告:模型申请的工具不存在!!!"
        self.memory.save_history(message[1:])
        return "轮次已用完"
