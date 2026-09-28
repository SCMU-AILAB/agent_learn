from tools.tool import combine

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

@combine
class Cale:
    name="cale"
    tol=cale
    tool_explain=[
        {
            "type":"function",
            "function":
            {
                "name":name,
                "description":"当用户提出要计算时调用该工具,适用于加减乘除数学表达式。",
                "parameters":
                {
                    "type":"object",
                    "properties":
                    {
                        "expr":
                        {
                            "type":"string",
                            "description":"数学表达式，例如1+1"
                        }
                    },
                    "required":["expr"]
                }
            }
        }
    ]
