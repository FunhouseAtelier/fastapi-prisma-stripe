# app/utils/flash.py

from fastapi import Request


def get_flashes(request: Request) -> list[str]:
    return request.session.pop("flash", [])


def set_flash(request: Request, messages: list[str]):
    request.session["flash"] = messages
