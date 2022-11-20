from typing import Optional
from pydantic import BaseModel

class messageRequest(BaseModel):
    token: str
    message: str