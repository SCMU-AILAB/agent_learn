from datetime import datetime

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