# app/schemas/product.py

from typing import Annotated

from pydantic import Field

from app.schemas._common import FullNameStr

__all__ = [
    "FullNameStr",
]

ProductDescriptionStr = Annotated[
    str,
    Field(
        min_length=3,
        max_length=1000,
    ),
]

UnitStr = Annotated[str, Field(min_length=2, max_length=10)]

UnitPriceInt = Annotated[int, Field()]
