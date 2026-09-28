import os
import requests

API_KEY  = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
MODEL    = os.getenv("MODEL", "deepseek-chat")


def ask(messages, tools=None):
    body = {"model": MODEL, "messages": messages}
    if tools:
        body["tools"] = tools
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=body, timeout=120,
    )
    resp.raise_for_status()
    msg = resp.json()["choices"][0]["message"]
    return {k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")}