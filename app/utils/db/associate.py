# app/utils/db/associate.py

from app.utils.format import encode_id
from app.utils.prisma import prisma
from app.utils.security import generate_salt
from app.utils.validators.id import validate_id58_to_id

# read all/filtered associate records
async def read_all_associates(where={}):
    try:
        associates = await prisma.associate.find_many(
            where=where, order={"updated_at": "desc"})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    # Prepare separate id58 mapping
    id58_by_id = {
        associate.id: encode_id(associate.id)
        for associate in associates
    }

    return {
        "success": {
            "associates": associates,
            "id58_by_id": id58_by_id,
        }
    }

# read one associate record
async def read_one_associate(id58):
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
        associate = await prisma.associate.find_unique(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}
    if not associate:
        return {"failure": {"type": "not_found", "msg": "Associate not found"}}

    return {
        "success": {
            "associate": associate,
            "id58": encode_id(associate.id)
        }
    }

# create a new associate record
async def create_associate(data):
    try:
        data["salt"] = generate_salt()
        associate = await prisma.associate.create(data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {
        "success": {
            "associate": associate,
            "id58": encode_id(associate.id)
        }
    }

# update an associate record
async def update_associate(id58, data):
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
        associate = await prisma.associate.update(where={"id": id}, data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {
        "success": {
            "associate": associate,
            "id58": encode_id(associate.id)
        }
    }

# destroy an associate record
async def delete_associate(id58):

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
        await prisma.associate.delete(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": True}

async def get_associate_by_username(username: str):
    return await prisma.associate.find_unique(where={"username": username})
