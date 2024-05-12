from backend.dependencies import (
    FastAPI,
    Request,
    HTTPException,
    Depends,
    format_stack_trace,
    LogManager,
    Config,
    CORSMiddleware, JSONResponse
)
from backend.routers.APIrouter import api
from backend.events import ApplicationEvent

app = FastAPI(title="Furina 网站API",version="0.0.1",description="一个用于 Furina 网站的API")
logger = LogManager.GetLogger('main')

for event_name , func in ApplicationEvent.event_dict.items():
    app.add_event_handler(event_name,func)
    logger.debug(f"已注册事件 {event_name}")

@app.exception_handler(Exception)
async def global_exception_handler(request:Request, exc:Exception):
    stack_infos = format_stack_trace(type(exc), exc,exc.__traceback__)
    logger.critical(stack_infos)
    return JSONResponse(status_code=500, content={"message": "服务器发生了一些错误，已联系管理员"})

# 允许所有CORS跨越资源共享的中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if Config.DEBUG_MODE == True:
    pass
else:
    app.openapi_url = None

app.include_router(api,tags=["Furina API"])