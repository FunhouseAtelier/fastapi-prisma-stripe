# app/routes/associate.py

# from fastapi import APIRouter, HTTPException
# from prisma_client.models import Associate

# from app.schemas.associate import AssociateCreateSchema, AssociateUpdateSchema

# router = APIRouter(prefix="/api/associate", tags=["associate"])

# @router.get("/", response_model=list[Associate])
# async def list_associates():
#     return await Associate.prisma().find_many()

# @router.get("/{associate_id}", response_model=Associate)
# async def get_associate(associate_id: str):
#     associate = await Associate.prisma().find_unique(where={"id": associate_id})
#     if not associate:
#         raise HTTPException(status_code=404, detail="Associate not found")
#     return associate

# @router.post("/", response_model=Associate)
# async def create_associate(data: AssociateCreateSchema):
#     return await Associate.prisma().create(data=data.model_dump())

# @router.put("/{associate_id}", response_model=Associate)
# async def update_associate(associate_id: str, data: AssociateUpdateSchema):
#     existing = await Associate.prisma().find_unique(where={"id": associate_id})
#     if not existing:
#         raise HTTPException(status_code=404, detail="Associate not found")
#     return await Associate.prisma().update(where={"id": associate_id}, data=data.model_dump())

# @router.delete("/{associate_id}", response_model=Associate)
# async def delete_associate(associate_id: str):
#     existing = await Associate.prisma().find_unique(where={"id": associate_id})
#     if not existing:
#         raise HTTPException(status_code=404, detail="Associate not found")
#     return await Associate.prisma().delete(where={"id": associate_id})
