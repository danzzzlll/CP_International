from pydantic_settings import BaseSettings

class Config(BaseSettings):
    pass

    class Config:
        env_prefix = "APP_"
