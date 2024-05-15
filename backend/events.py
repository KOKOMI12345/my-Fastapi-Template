from backend.dependencies import Config , LogManager,wraps
from backend.utils.dbController import Databasepool
from backend.Interfaces import EventInterface
from backend.exceptions import EventsAlreadyRegisted
from typing import Callable , Any
logger = LogManager.GetLogger('events')

class AppEvent(EventInterface):
    def __init__(self) -> None:
        self.event_dict: dict[str, Callable[...,Any]] = {}

    def register_event(self,event_name: str):
        """ 装饰器 """
        def decorator(func: Callable[...,Any]) -> Callable[...,Any]:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            if event_name not in self.event_dict:
               self.event_dict[event_name] = wrapper
            else:
                raise EventsAlreadyRegisted(f"事件 {event_name} 已经注册!")
            return wrapper
        return decorator

    def get_all_events(self) -> dict[str, Callable[...,Any]]:
        return self.event_dict
    
ApplicationEvent = AppEvent()

@ApplicationEvent.register_event('startup')
async def startup():
    logger.info(f"Furina 网站API 启动成功,API后端程序开启,服务器运行在: http://{Config.HOST}:{Config.PORT}")
    await Databasepool.Initialize()

@ApplicationEvent.register_event('shutdown')
async def shutdown():
    logger.info("Furina 网站API 关闭成功")
    await Databasepool.close()