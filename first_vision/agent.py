import json
from datetime import datetime

from llm import ask

def get_time(city):
    return f"{city}时间:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def cale(expr):
    if all(x in "1234567890/*-+()" for x in expr):#这里用白名单做边界
        return f"{expr}={eval(expr)}"
    else:
        error=[]
        for x in expr:
            if x not in "1234567890/*-+()":
                error.append(x)
            else:
                continue
        return f"警告:非法输入!!!  非法字符:{error}"

tool_explain = [   
    {
        "type": "function",
        "function":    
        {
            "name": "cale",
            "description": "当用户提出要计算时调用该工具,适用于加减乘除数学表达式",
            "parameters": 
            {
                "type": "object",
                "properties": 
                {
                    "expr": 
                    {
                        "type": "string",
                        "description": "数学表达式，例如：1+1。"
                    }
                },
                "required":["expr"]
            }
        }
    },

    {
        "type": "function",
        "function": 
        {
            "name": "get_time",
            "description": "查询某个城市化当前的日期和时间，用户问：现在几点或某个城市的时间时使用。",
            "parameters": 
            {
                "type": "object",
                "properties": 
                {
                    "city": 
                    {
                        "type": "string",
                        "description": "城市名，例如北京。"
                    }
                },
                "required":["city"]
            }
        }
    }
]

tool_list={
    "get_time":get_time,
    "cale":cale,
}

def to_run(questions):
    message=[
        {"role": "system", "content": "回答要简洁，直接给结论，不要展开推导过程。"},
        {"role":"user","content":questions}
    ]

    epochs=8
    count=0

    for i in range(epochs):
        count+=1
        answers = ask(message,tools=tool_explain)
        message.append(answers)

        apply_list=answers.get("tool_calls") or []

        if apply_list==[]:
            print(f"运行{count}次")
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

if __name__ == "__main__":
    print(to_run("北京现在几点？顺便算一下 (23*7+15)/2"))