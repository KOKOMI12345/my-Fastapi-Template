from backend.furinaApp import app
import uvicorn
from backend.config import Config

if __name__ == "__main__":
   try:
      uvicorn.run(app, host=Config.HOST, port=Config.PORT,log_level="critical")
   except KeyboardInterrupt:
      pass