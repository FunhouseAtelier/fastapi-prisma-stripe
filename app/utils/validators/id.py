# app/validators/id.py

from app.utils.format import decode_id58


async def validate_id58_to_id(id58: str):
    try:
        id = decode_id58(id58)
    except Exception as e:
        return {"failure": {"type": "validation", "detail": str(e)}}

    return {"success": {"id": id}}
