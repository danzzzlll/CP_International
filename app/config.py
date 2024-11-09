from pydantic_settings import BaseSettings

class Config(BaseSettings):
    device_map: str = "sequential"
    load_in_8bit: bool = True
    max_new_tokens: int = 128
    do_sample: bool = True
    num_beams: int = 1
    temperature: float = 0.25
    top_k: int = 50
    top_p: float = 0.98
    eos_token_id: int = 79097

    class Config:
        env_prefix = "APP_"
