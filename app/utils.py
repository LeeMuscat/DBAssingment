from bson import ObjectId

def oid(id_str: str) -> ObjectId:
    return ObjectId(id_str)

def fix_id(doc: dict) -> dict:
    """Convert Mongo _id to string id for JSON responses."""
    if not doc:
        return doc
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc
