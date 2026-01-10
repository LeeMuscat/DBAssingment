from fastapi import FastAPI
from app.db.mongodb import db
from app.routes.events import router as events_router

app = FastAPI(title="Event Management API")

@app.get("/")
def root():
    return {"status": "connected", "collections": db.list_collection_names()}

app.include_router(events_router)
