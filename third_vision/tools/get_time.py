# third_vision/tools/get_time.py
"""时间工具：按城市名返回本机当前时间（不做时区换算）."""

from datetime import datetime

from .tool_register import tr, ToolPolicy


@tr.register(
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "查询某个城市化当前的日期和时间，用户问：现在几点或某个城市的时间时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，例如北京。"}
                },
                "required": ["city"],
            },
        },
    },
    ToolPolicy(
        read_only=True,
        idempotent=True
    )
)
def get_time(city):
    return f"{city}时间:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
