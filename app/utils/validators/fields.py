# app/validators/fields.py

from typing import Optional

from pydantic import BaseModel


def trim_one_string(value):
    if isinstance(value, str):
        return value.strip()
    return value


def format_one_phone_number(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    digits = "".join(filter(str.isdigit, value))
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return value


def make_one_string_lowercase(value: str) -> str:
    return value.lower()


def format_one_ssn(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    digits = "".join(filter(str.isdigit, value))
    if len(digits) == 9:
        return f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"
    return value


def format_one_tin(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    digits = "".join(filter(str.isdigit, value))
    if len(digits) == 9:
        return f"{digits[:2]}-{digits[2:]}"
    return value


def coerce_one_string_to_list(value):
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        return [v for v in value if v]  # filter out any falsy values
    return []


def require_one_field(model: BaseModel, fields: list[str]) -> bool:
    for field in fields:
        value = getattr(model, field, None)
        if value:
            return True
    return False


def unset_if_empty(value: Optional[str]):
    if value is None or not str(value).strip():
        return {"unset": True}
    return value
