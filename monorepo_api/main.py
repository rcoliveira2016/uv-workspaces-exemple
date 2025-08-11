from monorepo_core.config import config_core;
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Olá do monorepo_api com FastAPI!", "config": config_core.api_url}