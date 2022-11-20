from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    user: str
    token: str