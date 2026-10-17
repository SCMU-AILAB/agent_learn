# third_vision/llm.py
"""模型接口：把消息和工具说明书发出去，拿回模型的一条回复（只留 role/content/tool_calls）."""

import os
import requests

from config import TOOL_TIMEOUT

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
MODEL = os.getenv("MODEL", "deepseek-chat")


def ask(messages, tools=None):
    body = {"model": MODEL, "messages": messages}
    if tools:
        body["tools"] = tools
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=body,
        timeout=TOOL_TIMEOUT,
    )

    resp.raise_for_status()
    msg = resp.json()["choices"][0]["message"]
    return {k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")}
