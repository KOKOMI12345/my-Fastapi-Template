from backend.dependencies import APIRouter , Depends, HTTPException
from backend.utils.security import Security
from backend.datamodels.usermodel import User
from backend.utils.UserControllers import login_user , register_user , ChangePassword

api = APIRouter(prefix="/api")

# 这下面用于定义API路由

@api.get("/")
async def root() -> dict:
    return {"message": "Hello from my API endpoint"}

@api.post("/login")
async def login(user: User) -> dict:
    result = await login_user(username=user.username, password=user.password)
    if result == True:
        payload = {
            "username": user.username,
            "password": user.password
        }
        return {"status": 200, "message": "登录成功", "token": await Security.generate_token(payload)}
    elif result == "password error":
        return {"status": 400, "message": "密码错误"}
    else:
        raise HTTPException(status_code=500, detail="服务器错误")

@api.post("/register")
async def register(user: User) -> dict:
    result = await register_user(username=user.username, password=user.password)
    if result == "is_exist":
        raise HTTPException(status_code=400, detail="用户名已存在")
    elif result == "success":
        payload = {
            "username": user.username,
            "password": user.password
        }
        return {"status": 200, "message": "注册成功", "token": await Security.generate_token(payload)}
    else:
        raise HTTPException(status_code=500, detail="服务器错误")
    
@api.post("/change_password")
async def change_password(user: User, token: tuple[bool,str] = Depends(Security.verify_token)) -> dict:
    if token[0] == True:
        result = await ChangePassword(username=user.username, new_password=user.password)
        if result == True:
            payload = {
                "username": user.username,
                "password": user.password
            }
            return {"status": 200, "message": "密码修改成功", "token": await Security.generate_token(payload)}
        elif result == "user not exist":
            raise HTTPException(status_code=400, detail="用户名不存在")
        else:
            raise HTTPException(status_code=500, detail="服务器错误")
    else:
        err_msg = token[1]
        raise HTTPException(status_code=401, detail=err_msg)