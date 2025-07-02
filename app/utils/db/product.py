# app/utils/db/product.py

from app.utils.format import encode_id
from app.utils.prisma import prisma
from app.utils.validators.id import validate_id58_to_id


# read all/filtered product records
async def read_all_products(where={}):
    try:
        products = await prisma.product.find_many(where=where,
                                                  order={"updated_at": "desc"})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    # Prepare separate id58 mapping
    id58_by_id = {product.id: encode_id(product.id) for product in products}

    return {
        "success": {
            "products": products,
            "id58_by_id": id58_by_id,
        }
    }


# read one product record
async def read_one_product(id58):
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
        product = await prisma.product.find_unique(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}
    if not product:
        return {"failure": {"type": "not_found", "msg": "Product not found"}}

    return {"success": {"product": product, "id58": encode_id(product.id)}}


# create a new product record
async def create_product(data):
    try:
        product = await prisma.product.create(data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"product": product, "id58": encode_id(product.id)}}


# update an product record
async def update_product(id58, data):
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
        product = await prisma.product.update(where={"id": id}, data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"product": product, "id58": encode_id(product.id)}}


# destroy an product record
async def delete_product(id58):

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
        await prisma.product.delete(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": True}
