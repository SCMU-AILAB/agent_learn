# third_vision/config.py
"""集中管理运行配置."""

MAX_ITERATIONS = 8        # 最多问模型几轮
MAX_TOOL_CALLS = 24       # 一次对话最多调几次工具
TOOL_TIMEOUT = 120        # 单次请求超时（秒）
MAX_SAME_CALL_REPEATS = 2
