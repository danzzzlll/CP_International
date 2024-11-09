from pydantic import BaseModel

class InputData(BaseModel):
    topic: str
    description: str

class ResponseData(BaseModel):
    topic: str
    description: str
    device: str
    failure_point: str
    serial_number: str
