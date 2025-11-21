from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    """Esquema base para respuestas"""
    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    database: str
    version: str

class InfoResponse(BaseModel):
    api_name: str
    version: str
    description: str
    modules: list[str]
    data_sources: list[str]
    contact: dict