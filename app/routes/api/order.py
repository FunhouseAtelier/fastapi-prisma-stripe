# app/routes/order.py

# from fastapi import APIRouter, HTTPException
# from prisma_client.models import Order
# from app.schemas.order import OrderCreate, OrderUpdate

# router = APIRouter(prefix="/api/order", tags=["order"])

# @router.get("/", response_model=list[Order])
# async def list_orders():
#     return await Order.prisma().find_many()

# @router.get("/{order_id}", response_model=Order)
# async def get_order(order_id: str):
#     order = await Order.prisma().find_unique(where={"id": order_id})
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order

# @router.post("/", response_model=Order)
# async def create_order(data: OrderCreate):
#     return await Order.prisma().create(data=data.dict())

# @router.put("/{order_id}", response_model=Order)
# async def update_order(order_id: str, data: OrderUpdate):
#     existing = await Order.prisma().find_unique(where={"id": order_id})
#     if not existing:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return await Order.prisma().update(where={"id": order_id}, data=data.dict())

# @router.delete("/{order_id}", response_model=Order)
# async def delete_order(order_id: str):
#     existing = await Order.prisma().find_unique(where={"id": order_id})
#     if not existing:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return await Order.prisma().delete(where={"id": order_id})
