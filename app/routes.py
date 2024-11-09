from fastapi import APIRouter
from .models import InputData, ResponseData
from .utils import generate_response

router = APIRouter()

@router.post("/generate", response_model=ResponseData)
async def generate(data: InputData):
    response_data = generate_response(
        data.topic,
        data.description
    )
    return response_data
