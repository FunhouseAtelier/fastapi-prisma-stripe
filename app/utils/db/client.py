# app/utils/db/client.py

from app.utils.format import encode_id
from app.utils.prisma import prisma
from app.utils.security import generate_account_number
from app.utils.validators.id import validate_id58_to_id


# read all/filtered client records
async def read_all_clients(where={}):
    try:
        clients = await prisma.client.find_many(where=where,
                                                order={"updated_at": "desc"})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    # Prepare separate id58 mapping
    id58_by_id = {client.id: encode_id(client.id) for client in clients}

    return {
        "success": {
            "clients": clients,
            "id58_by_id": id58_by_id,
        }
    }


# read one client record
async def read_one_client(id58):
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
        client = await prisma.client.find_unique(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}
    if not client:
        return {"failure": {"type": "not_found", "msg": "Client not found"}}

    return {"success": {"client": client, "id58": encode_id(client.id)}}


# create a new client record
async def create_client(data):
    try:
        data["account_number"] = await generate_account_number()
        client = await prisma.client.create(data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"client": client, "id58": encode_id(client.id)}}


# update an client record
async def update_client(id58, data):
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
        client = await prisma.client.update(where={"id": id}, data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"client": client, "id58": encode_id(client.id)}}


# destroy an client record
async def delete_client(id58):

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
        await prisma.client.delete(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": True}
