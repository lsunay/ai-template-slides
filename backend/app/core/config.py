from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    app_name: str = "AI Template Slides API"
    debug: bool = False
    
    # OpenAI Settings
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    
    # Ollama Settings
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "mistral:instruct"
    
    # LM Studio Settings
    lmstudio_host: str = "http://localhost:1234"
    
    # File Storage
    output_dir: str = "./outputs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()