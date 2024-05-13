from backend.dependencies import os , LogManager,hashlib
from backend.utils.dbController import GetDBConnectionContext
from typing import Optional,Union

logger = LogManager.GetLogger('mysql')

async def register_user(username: str, password: str) -> Optional[str]:
    logger.info(f"尝试注册用户: {username}")
    try:
        async with GetDBConnectionContext() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT COUNT(*) FROM user WHERE username=%s", (username,))
                result = await cur.fetchone()
                if result[0] > 0:  # 如果存在重复用户名，则返回 False
                    logger.warning(f"用户名 {username} 已存在，注册失败")
                    return "is_exist"
                
                salt = os.urandom(32)
                hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                logger.debug(f"注册用户: {username}, 密码: {password}, 盐值: {salt.hex()},密码哈希: {hashed_password.hex()}")

                await cur.execute("INSERT INTO user (username, password, salt) VALUES (%s, %s, %s)", (username, hashed_password, salt))
            await conn.commit()
            logger.info(f"用户 {username} 注册成功")
            return "success"
        
    except Exception as e:
        logger.error(f"注册用户时发生错误: {e}",exc_info=True)
        return "error"
    
async def login_user(username: str, password: str) -> Union[bool,str]:
    logger.info(f"尝试登录用户: {username}")
    try:
        async with GetDBConnectionContext() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM user WHERE username=%s", (username,))
                result = await cur.fetchone()
                if result:
                    stored_password: bytes = result[2]  # 获取数据库中存储的哈希密码
                    salt: bytes = result[3]  # 获取数据库中存储的盐值
                    logger.debug(f"获取到用户 {username} 的密码哈希和盐值：{stored_password.hex()}, {salt.hex()}")
                    # 对用户输入的密码进行相同的哈希操作
                    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).rstrip(b'\0')
                    logger.debug(f"计算出用户 {username} 的密码哈希：{hashed_password.hex()}")
                    # 比较哈希后的密码是否一致
                    if hashed_password.hex() == stored_password.hex():
                        logger.info(f"用户: {username} 登录成功")
                        return True
                    else:
                        logger.info(f"用户: {username} 密码错误")
                        return "password error"
                else:
                    logger.info(f"用户: {username} 不存在")
                    return False
                
    except Exception as e:
        logger.error(f"登录用户时发生错误: {e}",exc_info=True)
        return "error"

async def ChangePassword(username: str, new_password: str) -> Union[bool,str]:
    try:
        async with GetDBConnectionContext() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM user WHERE username=%s", (username,))
                result = await cur.fetchone()
                if result:
                    salt = os.urandom(32)
                    # 对用户输入的密码进行相同的哈希操作
                    hashed_password = hashlib.pbkdf2_hmac('sha256', new_password.encode('utf-8'), salt, 100000)
                    logger.debug(f"用户: {username} 更改密码: {new_password}, 密码哈希: {hashed_password.hex()}")
                    await cur.execute("UPDATE user SET password=%s, salt=%s WHERE username=%s", (hashed_password, salt, username))
                    await conn.commit()
                    logger.info(f"用户: {username} 更改密码成功")
                    return True
                
                else:
                    logger.warning(f"用户: {username} 不存在")
                    return "user not exist"
        
    except Exception as e:
        logger.error(f"更改密码时发生错误: {e}",exc_info=True)
        return "error"