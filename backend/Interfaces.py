from backend.dependencies import ABC , abstractmethod
from typing import Any, Callable

# 这里用于声名接口类

class EventInterface(ABC):
    """
    事件接口类,可以理解为一个规范
    """
    @abstractmethod
    def __init__(self) -> None: ...

    @abstractmethod
    def register_event(self,func: Callable[...,Any],event_name: str): ...

    @abstractmethod
    def get_all_events(self) -> dict[str, Callable[...,Any]]: ...