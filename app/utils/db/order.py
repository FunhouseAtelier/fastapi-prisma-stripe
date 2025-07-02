# app/utils/db/order.py

from app.utils.format import encode_id
from app.utils.prisma import prisma
from app.utils.validators.id import validate_id58_to_id


# read all/filtered order records
async def read_all_orders(where={}):
    try:
        orders = await prisma.order.find_many(where=where,
                                              order={"updated_at": "desc"})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    # Prepare separate id58 mapping
    id58_by_id = {order.id: encode_id(order.id) for order in orders}

    return {
        "success": {
            "orders": orders,
            "id58_by_id": id58_by_id,
        }
    }


# read one order record
async def read_one_order(id58):
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
        order = await prisma.order.find_unique(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}
    if not order:
        return {"failure": {"type": "not_found", "msg": "Order not found"}}

    return {"success": {"order": order, "id58": encode_id(order.id)}}


# create a new order record
async def create_order(data: dict):
    client_id = data["client_id"]

    try:
        # Step 1: Look up latest order for this client (sorted by invoice_number descending)
        latest = await prisma.order.find_first(
            where={"client_id": client_id},
            order={"invoice_number": "desc"},
        )

        # Step 2: Extract numeric suffix and increment
        if latest and latest.invoice_number:
            base_prefix = latest.invoice_number.rsplit("-", 1)[0]
            suffix_str = latest.invoice_number.rsplit("-", 1)[-1]
            try:
                suffix_int = int(suffix_str)
            except ValueError:
                suffix_int = 0
        else:
            # default prefix from client account_number
            client = await prisma.client.find_unique(where={"id": client_id})
            if not client or not client.account_number:
                return {
                    "failure": {
                        "type": "db",
                        "msg": "Client not found or missing account_number",
                    }
                }
            base_prefix = client.account_number
            suffix_int = 0

        # Step 3: Format new invoice number
        new_suffix = f"{suffix_int + 1:04}"
        invoice_number = f"{base_prefix}-{new_suffix}"

        order_data = {
            "invoice_number": invoice_number,
            "status": data["status"],
            "sales_tax": data["sales_tax"],
            "total_due": 0,
            "transaction_fee": 0,
            "revenue": 0,
            "audited_at": data["audited_at"],
            "audit_notes": data.get("audit_notes") or "",
            "client": {
                "connect": {
                    "id": client_id
                }
            },
            "sales_associates": {
                "connect": [{
                    "id": id
                } for id in data.get("sales_associate_ids", [])]
            },
            "tech_associates": {
                "connect": [{
                    "id": id
                } for id in data.get("tech_associate_ids", [])]
            },
        }

        # Only add if present
        if data.get("audited_by_id"):
            order_data["audited_by"] = {
                "connect": {
                    "id": data["audited_by_id"]
                }
            }

        order = await prisma.order.create(data=order_data)

        return {"success": {"order": order, "id58": encode_id(order.id)}}

    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}


# async def create_order(data):
#     try:
#         order = await prisma.order.create(data=data)
#     except Exception as e:
#         return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

#     return {"success": {"order": order, "id58": encode_id(order.id)}}


# update an order record
async def update_order(id58, data):
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
        order = await prisma.order.update(where={"id": id}, data=data)
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": {"order": order, "id58": encode_id(order.id)}}


# destroy an order record
async def delete_order(id58):

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
        await prisma.order.delete(where={"id": id})
    except Exception as e:
        return {"failure": {"type": "db", "msg": f"Database error: {str(e)}"}}

    return {"success": True}
