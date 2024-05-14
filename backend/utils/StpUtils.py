from backend.dependencies import wraps
from backend.exceptions import PermissionAlreadyExists , PermissionFuncNotExists
from typing import Callable,Any
from backend.plugins.helpers import IsTesting

"""
这个模块用于实现不同路由通过不同的验证逻辑的算法，比如:
@api.get("/user")
@HasRole.checkPermission("user")
async def get_some() -> dict: ...
"""

class HasRole:
    """
    实现不同路由通过不同的验证逻辑
    """
    registed_permission_dict: dict[str,Callable[...,Any]] = {}

    @IsTesting()
    @classmethod
    def registerPermission(cls,role: str):
        """ 注册验证权限装饰器 """
        def decorator(func: Callable[...,Any]) -> Callable[...,Any]:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if role in cls.registed_permission_dict:
                    raise PermissionAlreadyExists(f"权限验证函数{role}已存在")
                else:
                    return await func(*args, **kwargs)
            cls.registed_permission_dict[role] = wrapper
            return wrapper
        return decorator
    
    @IsTesting()
    @classmethod
    def checkPermission(cls, role: str) -> Callable[..., Any]:
        """
        获取权限验证函数,类似Java的
        匹配路由，然后通过不同的权限验证的逻辑
        """
        async def wrapper(*args, **kwargs):
            if role in cls.registed_permission_dict:
                return await cls.registed_permission_dict[role](*args, **kwargs)
            else:
                raise PermissionFuncNotExists(f"权限验证函数{role}不存在")
        return wrapper

@IsTesting()
class Exclude:
    """
    这个只是声明一个注解，就是，
    被声明的路由代表可以直接访问，
    不需要权限验证的注解
    """
    def __call__(self,func: Callable[..., Any]) -> Callable[..., Any]:
        return func