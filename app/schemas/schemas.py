from pydantic import BaseModel
from typing import Optional

class MathRequest(BaseModel):
    x: int
    y: Optional[int] = None  # Used for pow(); ignored for factorial/fibonacci

class MathResponse(BaseModel):
    operation: str
    input: str
    result: float
