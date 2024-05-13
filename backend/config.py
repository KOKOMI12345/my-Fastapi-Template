

# 配置文件

class Config:
    """配置类"""
    DEBUG_MODE = True
    HOST = '127.0.0.1'
    PORT = 5000
    secret_key = 'furina-fastapi-app-backend'
    algorithm = 'HS256'
    expire_time_day = 7 
    allowfile = ['jpg', 'png', 'jpeg', 'gif','zip','rar','7z','doc','docx','xls','xlsx','ppt','pptx','pdf','mp4','mp3','wav','aac']
    validate_token_level = "decode" # 设置token验证登记,可以设置为 decode或verify

class DatabaseConfig:
    """数据库配置类"""
    HOST = 'localhost'
    PORT = 3306
    USER = 'root'
    PASSWORD = '123456'
    DB = 'furina'
    CHARSET = 'utf8mb4'
    MAX_SIZE = 20 # 最大连接数