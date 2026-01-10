from fastapi import FastAPI
from app.db.mongodb import db
from app.routes.events import router as events_router

app = FastAPI(title="Event Management API")

@app.get("/")
async def root():
    collections = await db.list_collection_names()
    return {"status": "connected", "collections": collections}

app.include_router(events_router)
