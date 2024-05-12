from backend.dependencies import asynccontextmanager, DatabaseConfig , aiomysql , DatabaseException
from backend.utils.databasePool import DatabasePool

Databasepool = DatabasePool(DatabaseConfig.MAX_SIZE)
    
@asynccontextmanager
async def GetDBConnectionContext():
    """
    获取一个数据库连接的上下文管理器
    """
    conn = await Databasepool.GetConnection()
    try:
        if isinstance(conn, aiomysql.Connection):
            yield conn
        else:
            raise DatabaseException("获取数据库连接失败")
    finally:
        if isinstance(conn, aiomysql.Connection):
            await Databasepool.ReleaseConnection(conn)