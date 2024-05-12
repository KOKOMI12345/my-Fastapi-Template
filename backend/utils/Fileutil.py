from backend.dependencies import os , LogManager , aiofiles
from typing import AsyncGenerator, Any

class Fileutil:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = LogManager.GetLogger(self.__class__.__name__)

    @classmethod
    async def readFile(cls, file_path: str) -> bytes:
        async with aiofiles.open(file_path, mode='rb') as f:
            return await f.read()
        
    @classmethod
    async def writeFile(cls,file_path:str,byte: bytes) -> bool:
        try:
            async with aiofiles.open(file_path, mode='wb') as f:
                await f.write(byte)
                return True
        except Exception as e:
            return False
        
    @classmethod
    async def FileStream(cls,file_path: str,buffer_size: int = 1024) -> AsyncGenerator[bytes, Any]:
        """
        文件流读取
        """
        async with aiofiles.open(file_path, mode='rb') as f:
            while True:
                data = await f.read(buffer_size)
                if not data:
                    break
                yield data