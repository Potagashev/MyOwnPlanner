from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    BOT_TOKEN: str

    GIGACHAT_API_KEY: str
    GIGACHAT_CLIENT_ID: str
    GIGACHAT_CLIENT_SECRET: str

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    
    @property
    def database_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'

settings = Settings()
