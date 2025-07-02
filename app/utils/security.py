# app/utils/security.py

import random
import secrets
import hashlib
import hmac
from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import RedirectResponse
from functools import wraps
from typing import Callable, Union

from app.utils.prisma import prisma
from app.utils.envars import AUTH_STATUS

def has_role(request: Request, role: str) -> bool:
    associate_roles = request.session.get("roles", [])
    return role in associate_roles

def is_admin(request: Request) -> bool:
    return has_role(request, "admin")

def require_role(roles: Union[str, list[str]]) -> Callable:
    if isinstance(roles, str):
        roles = [roles]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Bypass role checks if auth is disabled
            if AUTH_STATUS == "disabled":
                return await func(request, *args, **kwargs)

            user_roles = request.session.get("roles", [])
            if not any(role in user_roles for role in roles):
                request.session["flash"] = ["Access denied."]
                return RedirectResponse("/", status_code=303)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def generate_salt(length: int = 32) -> str:
    return secrets.token_hex(length // 2)  # 32 hex chars = 16 bytes

async def generate_account_number(max_attempts: int = 10) -> str:
    """Generate a unique account number with format YYXXXXXXXXXX (e.g., 251234567890)."""
    year_prefix = datetime.now(timezone.utc).strftime("%y")

    for _ in range(max_attempts):
        suffix = f"{random.randint(0, 9999999999):010}"
        account_number = f"{year_prefix}{suffix}"

        # Check uniqueness in the database
        existing = await prisma.client.find_unique(
            where={"account_number": account_number})
        if not existing:
            return account_number

    raise RuntimeError(
        "Failed to generate a unique account number after multiple attempts.")

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, hashed: str, salt: str) -> bool:
    return hmac.compare_digest(hash_password(password, salt), hashed)
