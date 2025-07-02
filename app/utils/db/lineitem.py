# app/utils/db/lineitem.py

from app.utils.format import encode_id
from app.utils.prisma import prisma
from app.utils.security import generate_salt
from app.utils.validators.id import validate_id58_to_id


# read all/filtered lineitem records
async def read_all_lineitems(where={}):
    try:
        lineitems = await prisma.lineitem.find_many(
            where=where, order={"updated_at": "desc"})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    # Prepare separate id58 mapping
    id58_by_id = {
        lineitem.id: encode_id(lineitem.id)
        for lineitem in lineitems
    }

    return {
        "success": {
            "lineitems": lineitems,
            "id58_by_id": id58_by_id,
        }
    }


# read one lineitem record
async def read_one_lineitem(id58):
    result = await validate_id58_to_id(id58)
    if "failure" in result:
        return {
            "failure": {
                "type": "not_found",
                "msg": "Invalid ID58",
            }
        }
    id = result["success"]["id"]

    try:
        lineitem = await prisma.lineitem.find_unique(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}
    if not lineitem:
        return {"failure": {"type": "not_found", "msg": "Lineitem not found"}}

    return {"success": {"lineitem": lineitem, "id58": encode_id(lineitem.id)}}


# create a new lineitem record
async def create_lineitem(data):
    data["salt"] = generate_salt()
    try:
        lineitem = await prisma.lineitem.create(data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"lineitem": lineitem, "id58": encode_id(lineitem.id)}}


# update an lineitem record
async def update_lineitem(id58, data):
    result = await validate_id58_to_id(id58)
    if "failure" in result:
        return {
            "failure": {
                "type": "not_found",
                "msg": "Invalid ID58",
            }
        }
    id = result["success"]["id"]

    try:
        lineitem = await prisma.lineitem.update(where={"id": id}, data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"lineitem": lineitem, "id58": encode_id(lineitem.id)}}


# destroy an lineitem record
async def delete_lineitem(id58):

    result = await validate_id58_to_id(id58)
    if "failure" in result:
        return {
            "failure": {
                "type": "not_found",
                "msg": "Invalid ID58",
            }
        }
    id = result["success"]["id"]

    try:
        await prisma.lineitem.delete(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": True}
