# app/utils/session.py

from fastapi import Request
from app.utils.db.associate import read_one_associate

async def create_session(request: Request, id58):
    
    result = await read_one_associate(id58)
    if "failure" in result:
        return
    associate = result["success"]["associate"]

    request.session["id58"] = result["success"]["id58"]
    request.session["roles"] = associate.roles
    request.session["sales_client_ids"] = associate.sales_client_ids
    request.session["tech_client_ids"] = associate.tech_client_ids
    request.session["sales_order_ids"] = associate.sales_order_ids
    request.session["tech_order_ids"] = associate.tech_order_ids

def force_password_reset_required(request: Request):
    request.session["must_reset_password"] = True

def clear_session(request: Request):
    request.session.clear()
