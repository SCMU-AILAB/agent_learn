# third_vision/tools/__init__.py
"""工具包的门：import 各工具模块以完成注册，并对外只暴露 tr."""

from . import cale, get_time
from .tool_register import tr

__all__ = ["tr"]
