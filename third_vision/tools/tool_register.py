# third_vision/tools/tool_register.py
"""工具注册表：@tr.register 登记工具；schemas 给模型看菜单；call 按名字执行."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar


@dataclass(frozen=True)
class ToolPolicy:
    read_only: bool = False           # 只读 → 可以自动重试
    idempotent: bool = False          # 幂等 → 才有资格复用 / 重试
    needs_stop: str | None = None     # ★ 我们自己加的：持续性动作必须配停止（Move → StopMove）
    approval: str = "automatic"       # automatic / approval_required / forbidden

ToolFn = Callable[
    ...,
    Any,
]

F = TypeVar(
    "F",
    bound=ToolFn,
)

class ToolRegistry:
    """实现工具的注册，并合并返回成给语言模型的列表."""

    def __init__(self) -> None:
        """初始化一个字典并赋予它管理的职责."""
        self.registered_tools: dict[str, tuple[dict[str, Any], ToolFn, ToolPolicy]] = {}

    def register(self, schema: dict[str, Any], toolpolicy: ToolPolicy) -> Callable[[F], F]:
        """
        装饰器工厂：传入 schema，返回一个真正的装饰器 deco

        Args:
            schema: dict[str, Any] => 工具函数的属性

        Returns:
            Callable[[F], F] => deco 接收什么类型的函数，就原样返回同一类型

        """
        def deco(fn: F) -> F:
            """
            decorator 函数 接受被修饰的函数 将工具函数记录到 registered_tools 字典中

            Args:
                fn: F => 传入的函数

            Returns:
                F => 返回同样类型

            """
            name = schema["function"]["name"]
            if name in self.registered_tools:
                raise ValueError(f"The {name} is used")
            self.registered_tools[name] = (schema, fn, toolpolicy)
            return fn

        return deco

    @property
    def schemas(self) -> list[dict[str, Any]]:
        """
        所有工具的 schema，喂给 vllm

        Returns:
            list[dict[str, Any]] => 所有工具的 schema
        """
        return [schema for schema, _, _ in self.registered_tools.values()]

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        """
        将 tool_calls 里的 name 分发执行

        Args:
            name: str                   => tool name
            arguments: dict[str, Any]   => 调用 tools 所需要的参数

        Returns:
            Any => tools 调用后的结果
        """

        if name not in self.registered_tools:
            return f"[Error]: unknown tool {name!r}" 
        _, fn, _ = self.registered_tools[name]

        try:
            return fn(**arguments)
        except Exception as e:
            return f"[Error]: {e}"


tr = ToolRegistry()
