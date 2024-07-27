from fastapi import FastAPI
from .routers import island
import logging

logging.getLogger().setLevel(logging.INFO)

app = FastAPI()

app.include_router(island.router)
