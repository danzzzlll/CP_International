from pydantic import BaseModel

class InputData(BaseModel):
    topic: str
    description: str

class ResponseData(BaseModel):
    created_at: str
    status: str
    topic: str
    description: str
    device: str
    failure_point: str
    serial_number: str
