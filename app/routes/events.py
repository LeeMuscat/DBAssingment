from fastapi import APIRouter, HTTPException, Request
from app.db.mongodb import db
from app.models.event import EventCreate, EventUpdate
from app.utils import oid, fix_id

router = APIRouter(prefix="/events", tags=["Events"])

events_col = db["Events"]  # <-- matches your existing collection name

@router.post("/")
def create_event(payload: EventCreate):
    doc = payload.model_dump()
    result = events_col.insert_one(doc)
    created = events_col.find_one({"_id": result.inserted_id})
    return fix_id(created)

@router.get("/")
def list_events():
    docs = list(events_col.find())
    return [fix_id(d) for d in docs]

@router.get("/{event_id}")
def get_event(event_id: str):
    try:
        doc = events_col.find_one({"_id": oid(event_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid event id")

    if not doc:
        raise HTTPException(status_code=404, detail="Event not found")
    return fix_id(doc)

@router.put("/{event_id}")
def update_event(event_id: str, payload: EventUpdate):
    try:
        _id = oid(event_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid event id")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    result = events_col.update_one({"_id": _id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    doc = events_col.find_one({"_id": _id})
    return fix_id(doc)

@router.delete("/{event_id}")
def delete_event(event_id: str):
    try:
        _id = oid(event_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid event id")

    result = events_col.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"status": "deleted", "id": event_id}
