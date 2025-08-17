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
    
    def get_database_url(self) -> str:
        db_url = (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )
        print(f"URL de conexión a la base de datos: {db_url}")
        return db_url 
    
settings = Settings()