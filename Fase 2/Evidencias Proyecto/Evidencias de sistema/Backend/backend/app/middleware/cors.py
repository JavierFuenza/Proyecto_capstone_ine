from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

def add_cors_middleware(app: FastAPI):
    """Agregar middleware CORS a la aplicación FastAPI"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )