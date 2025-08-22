from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    BASE_API_DOLAR: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    
    GMAIL_MAIL_PORT:int = 465
    GMAIL_MAIL_SERVER: str = "smtp.gmail.com"
    GMAIL_USERNAME: str
    GMAIL_PASSWORD: str
    GMAIL_SENDER_MAIL: str
    GMAIL_RECEIVER_MAIL: str
    
    def get_database_url(self) -> str:
        db_url = (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )
        print(f"URL de conexión a la base de datos: {db_url}")
        return db_url 
    
settings = Settings()