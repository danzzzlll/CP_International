from pydantic_settings import BaseSettings

class Config(BaseSettings):
    classifier: str = 'tfidf' # tfidf

    class Config:
        env_prefix = "APP_"
