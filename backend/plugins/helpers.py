from typing import Any
from backend.Bwarnings import TestingWarning , warnings
from backend.dependencies import wraps


# 测试装饰器,用于声名一个代码仍然在测试

class IsTesting:

    
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(f"{func.__name__} 函数或方法仍然在测试", TestingWarning,stacklevel=2)
            return await func(*args, **kwargs)
        return wrapper