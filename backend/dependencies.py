from SparkleLogging.utils.core import LogManager
import aiomysql , aiofiles
from typing import Any
from pydantic import BaseModel
import jwt,magic ,re ,time
from datetime import timedelta , datetime
from functools import wraps
from contextlib import asynccontextmanager
import os , hashlib , sys
from fastapi import FastAPI , Request , HTTPException , Depends , APIRouter
from fastapi import File,UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.excHandler import format_stack_trace
from backend.config import Config , DatabaseConfig
import asyncio
from backend.exceptions import DatabaseException
from abc import ABC,abstractmethod
import importlib