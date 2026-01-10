from fastapi import FastAPI, Request
from app.routes.events import router as events_router
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI(title="Event Management API")

@app.on_event("startup")
async def startup_db():
    app.state.mongo_client = AsyncIOMotorClient(os.environ["MONGO_URI"])
    app.state.db = app.state.mongo_client.leeMuscatDB

@app.on_event("shutdown")
async def shutdown_db():
    app.state.mongo_client.close()

@app.get("/")
async def root(request: Request):
    collections = await request.app.state.db.list_collection_names()
    return {"status": "connected", "collections": collections}

app.include_router(events_router)
