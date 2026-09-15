import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    qwen_model = os.getenv("QWEN_MODEL", "qwen-plus")
    qwen_api_key = os.getenv("DASHSCOPE_API_KEY", "")
    qwen_timeout = float(os.getenv("QWEN_TIMEOUT", "15"))
    detect_temperature = float(os.getenv("DETECT_TEMPERATURE", "0.2"))

settings = Settings()
