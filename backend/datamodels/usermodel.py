from backend.dependencies import BaseModel

class User(BaseModel):
    username: str
    password: str