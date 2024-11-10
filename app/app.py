from fastapi import FastAPI
from .config import Config
from .routes import router
from .classifier import inference_llm

# Initialize the configuration
config = Config()

# Initialize the FastAPI application
app = FastAPI()

# Include the API router
app.include_router(router)