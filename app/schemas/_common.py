# app/schemas/_common.py

from typing import Annotated

from pydantic import EmailStr, Field

# Full Name (letters, spaces, hyphens, apostrophes)
FullNameStr = Annotated[
    str,
    Field(min_length=2, max_length=100, pattern=r"^[A-Za-z][A-Za-z\s'\-]+$")]

# Business Name (trimmed, alphanumeric & symbols)
BusinessNameStr = Annotated[
    str,
    Field(min_length=2, max_length=100, pattern=r"^[A-Za-z0-9&.\-\s]+$")]

# Street Address (alphanumeric and common punctuation)
StreetStr = Annotated[
    str,
    Field(min_length=5, max_length=100, pattern=r"^[A-Za-z0-9#.\-\s]+$")]

# City (title-cased letters/spaces only)
CityStr = Annotated[
    str,
    Field(min_length=2, max_length=100, pattern=r"^[A-Za-z]+(?:\s[A-Za-z]+)*$"
          )]

# U.S. State Codes
USStateStr = Annotated[
    str,
    Field(
        pattern=
        r"^(A[LKZR]|C[AOT]|D[EC]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$"
    ),
]

# ZIP Code (US 5-digit or ZIP+4)
ZipCodeStr = Annotated[str, Field(pattern=r"^\d{5}(-\d{4})?$")]

# Phone Number (US 10-digit, no country code)
PhoneNumberStr = Annotated[str, Field(pattern=r"^\d{3}-\d{3}-\d{4}$")]

# Email (auto-trim/lowercase handled by Pydantic EmailStr)
EmailAddrStr = EmailStr
