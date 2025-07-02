# app/schemas/associate.py

from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from app.schemas._common import (
    BusinessNameStr,
    CityStr,
    EmailAddrStr,
    FullNameStr,
    PhoneNumberStr,
    StreetStr,
    USStateStr,
    ZipCodeStr,
)

__all__ = [
    "FullNameStr",
    "BusinessNameStr",
    "StreetStr",
    "CityStr",
    "USStateStr",
    "ZipCodeStr",
    "PhoneNumberStr",
    "EmailAddrStr",
]

# Username (3-24 chars, letters only, may contain - or _ but must start with letter)
UsernameStr = Annotated[
    str,
    Field(min_length=3, max_length=24, pattern=r"^[A-Za-z][A-Za-z_-]*$")]

# SSN: format as 123-45-6789
SSNStr = Annotated[str, Field(pattern=r"^\d{3}-\d{2}-\d{4}$")]

# TIN: same format 12-3456789
TINStr = Annotated[str, Field(pattern=r"^\d{2}-\d{7}$")]

# W-9 Date (required)
W9Date = datetime

# Roles (permissions)
RoleLiteral = Literal["admin", "sales", "tech"]

RolesList = Annotated[
    list[RoleLiteral],
    Field(description="Associate roles"),
]
