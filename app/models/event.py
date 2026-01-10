from pydantic import BaseModel, Field
from typing import Optional

class EventCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(0, ge=0)

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
