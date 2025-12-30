import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'llama2')
    PORT = int(os.getenv('PORT', 5000))