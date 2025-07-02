# app/schemas/client.py

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

# Account Status (limited to allowed statuses)
AccountStatusStr = Annotated[
    Literal["prospect", "active", "inactive", "suspended"],
    Field(description="Client account status"),
]
