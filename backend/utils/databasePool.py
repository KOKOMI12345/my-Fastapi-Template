from backend.dependencies import aiomysql , LogManager , DatabaseConfig , asyncio

class DatabasePool:
    def __init__(self, max_size: int = 10) -> None:
        self.max_size = max_size
        self.pool = asyncio.Queue(self.max_size)
        self.logger = LogManager.GetLogger(self.__class__.__name__)
        self.initiallzed = False

    async def GetConnection(self,timeout: float = 10.0) -> aiomysql.Connection | None:
        try:
            conn = await asyncio.wait_for(self.pool.get(),timeout=timeout)
            if isinstance(conn, aiomysql.Connection):
                return conn
            else:
                self.logger.warning("尝试获取非数据库连接")
                raise Exception("无法获取有效的数据库连接")
        except asyncio.TimeoutError:
            self.logger.warning("获取数据库连接超时")
            return None
    
    async def Is_initialized(self) -> bool:
        return self.initiallzed
    
    async def ReleaseConnection(self, connection: aiomysql.Connection) -> None:
        if not isinstance(connection, aiomysql.Connection):
            self.logger.warning("尝试释放非数据库连接")
            return
        await self.pool.put(connection)

    async def Initialize(self) -> None:
        self.logger.info("开始初始化数据库连接池")
        try:
            for _ in range(self.max_size):
                conn = await aiomysql.connect(
                    host=DatabaseConfig.HOST,
                    port=DatabaseConfig.PORT,
                    user=DatabaseConfig.USER,
                    password=DatabaseConfig.PASSWORD,
                    db=DatabaseConfig.DB,
                    charset=DatabaseConfig.CHARSET,
                )
                await self.pool.put(conn)
            self.logger.info("数据库连接池已初始化")
            self.initiallzed = True
        except Exception as e:
            self.logger.error(f"数据库连接池初始化失败: {e}")
            raise e

    async def __call__(self) -> None:
        # 初始化
        return await self.Initialize()
    
    async def close(self):
        # 关闭连接池,从连接池中陆陆续续释放连接
        while not self.pool.empty():
            try:
                conn = await self.pool.get()
                if isinstance(conn, aiomysql.Connection):
                    conn.close()
                else:
                    self.logger.warning("尝试释放非数据库连接")
            except Exception as e:
                self.logger.error(f"关闭连接时发生错误: {e}")
        self.logger.info("数据库连接池已关闭")