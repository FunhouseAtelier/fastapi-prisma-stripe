# app/utils/session.py

from fastapi import Request

def create_session(request: Request, associate_id: str):
    request.session["associate_id"] = associate_id

def force_password_reset_required(request: Request):
    request.session["must_reset_password"] = True

def clear_session(request: Request):
    request.session.clear()
