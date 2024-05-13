from backend.dependencies import jwt, timedelta , magic , Config,datetime , LogManager,re , asyncio,hashlib
from backend.utils.dbController import GetDBConnectionContext
from typing import Union
class Security:
    logger = LogManager.GetLogger('security')

    @staticmethod
    async def generate_token(payload: dict) -> str:
        """
        生成一个token
        """
        expire_time = timedelta(days=Config.expire_time_day)
        payload["exp"] = datetime.now() + expire_time
        return jwt.encode(payload, Config.secret_key, algorithm=Config.algorithm)
    
    @staticmethod
    async def verify_token(token: str,mode:str = "decode") -> tuple[bool,str]:
        """
        验证token
        """
        
        #验证token
        if mode == "decode":
            try:
                Security.logger.debug(f"开始验证token: {token}")
                decoded_token = await asyncio.to_thread(jwt.decode,token,Config.secret_key,algorithms=[Config.algorithm])
                return True, "验证成功"
            except jwt.ExpiredSignatureError:
                Security.logger.warning("token已过期")
                return False , "token已过期"
            except jwt.InvalidTokenError:
                Security.logger.warning("无效的token")
                return False , "无效的token"
            except Exception as e:
                Security.logger.error(f"token验证失败: {e}",exc_info=True)
                return False , "token验证失败"
        elif mode == "verify":
            result: tuple[bool,str] = await Security.verify_idinently(token)
            return result
        else:
            raise ValueError("无效的验证模式")
        
    @staticmethod
    async def verify_idinently(token: str) -> tuple[bool,str]: 
        """
        通过数据库验证身份,
        为了防止换了令牌后,原来的令牌仍然有效
        """
        Security.logger.debug(f"开始验证身份")
        payload: dict[str,str] = await asyncio.to_thread(jwt.decode,token,Config.secret_key,algorithms=[Config.algorithm])
        username: Union[str, None] = payload.get("username")
        password: Union[str, None] = payload.get("password")
        async with GetDBConnectionContext() as conn:
            async with conn.cursor() as cur:
                sql = "SELECT * FROM user WHERE username=%s"
                await cur.excute(sql,(username,))
                result = await cur.fetchone()
                if result:
                    stored_password: bytes = result[2]
                    salt: bytes = result[3]
                    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).rstrip(b'\0') #type: ignore
                    if stored_password.hex() == hashed_password.hex():
                        Security.logger.info("身份验证通过")
                        return True, "身份验证通过"
                    else:
                        Security.logger.warning("密码验证失败")
                        return False, "密码验证失败"
                else:
                    Security.logger.warning("用户不存在")
                    return False, "用户不存在"

        
    @staticmethod
    async def validate_file_type(file_data: bytes) -> tuple:
        file_type = magic.from_buffer(file_data, mime=False)
        if not file_type:
            Security.logger.error("无法获取文件类型信息")
            return  None, False, "file_type_error"

        simplified_file_type = re.match(r'^(\w+)', file_type)
        if not simplified_file_type:
            Security.logger.error(f"无法从文件类型中提取关键信息: {file_type}")
            return None, False, "file_type_error"

        simplified_file_type = simplified_file_type.group(1).lower()

        Security.logger.info(f"开始验证文件类型,允许的文件类型为: {Config.allowfile}")
        if simplified_file_type in Config.allowfile:
            Security.logger.info("文件类型验证通过")
            return simplified_file_type , True , "file_type_pass"
        else:
            Security.logger.warning(f"文件类型验证失败,验证到的类型: {simplified_file_type}")
            return simplified_file_type , False , "invalid_file_type"