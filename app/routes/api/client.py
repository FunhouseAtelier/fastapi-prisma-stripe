# app/routes/client.py

# from fastapi import APIRouter, HTTPException
# from prisma_client.models import Client
# from app.schemas.client import ClientCreate, ClientUpdate

# router = APIRouter(prefix="/api/client", tags=["client"])

# @router.get("/", response_model=list[Client])
# async def list_clients():
#     return await Client.prisma().find_many()

# @router.get("/{client_id}", response_model=Client)
# async def get_client(client_id: str):
#     client = await Client.prisma().find_unique(where={"id": client_id})
#     if not client:
#         raise HTTPException(status_code=404, detail="Client not found")
#     return client

# @router.post("/", response_model=Client)
# async def create_client(data: ClientCreate):
#     return await Client.prisma().create(data=data.dict())

# @router.put("/{client_id}", response_model=Client)
# async def update_client(client_id: str, data: ClientUpdate):
#     existing = await Client.prisma().find_unique(where={"id": client_id})
#     if not existing:
#         raise HTTPException(status_code=404, detail="Client not found")
#     return await Client.prisma().update(where={"id": client_id}, data=data.dict())

# @router.delete("/{client_id}", response_model=Client)
# async def delete_client(client_id: str):
#     existing = await Client.prisma().find_unique(where={"id": client_id})
#     if not existing:
#         raise HTTPException(status_code=404, detail="Client not found")
#     return await Client.prisma().delete(where={"id": client_id})
