# app/utils/validators/product.py

from decimal import Decimal, InvalidOperation
from typing import Optional

from fastapi import Request
from pydantic import BaseModel, ValidationError, field_validator

from app.schemas.product import (
    FullNameStr,
    ProductDescriptionStr,
    UnitPriceInt,
    UnitStr,
)
from app.utils.validators.fields import trim_one_string, unset_if_empty


class ProductFormSchema(BaseModel):
    name: FullNameStr
    description: Optional[ProductDescriptionStr] = None
    unit: UnitStr
    unit_price: UnitPriceInt

    @field_validator("*", mode="before")
    @classmethod
    def trim_string(cls, v):
        return trim_one_string(v)

    @field_validator("unit_price", mode="before")
    @classmethod
    def convert_price_to_cents(cls, v):
        try:
            if isinstance(v, str):
                # Normalize string input like "19.99"
                return int(Decimal(v) * 100)
            if isinstance(v, (float, Decimal)):
                return int(Decimal(v) * 100)
            if isinstance(v, int):
                return v  # already in cents
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid price format")
        raise ValueError("Invalid price format")

    @classmethod
    def with_unset(cls, data: dict):
        """Call this to apply `unset_if_empty` logic only for edit forms."""
        fields_to_check = ["description"]
        return cls(
            **{
                k: unset_if_empty(v) if k in fields_to_check else v
                for k, v in data.items()
            })


#
# USE IN ROUTE HANDLERS
#
async def validate_product_form(form_name: str, request: Request) -> dict:
    form = request.state.form
    try:
        if form_name == "new":
            parsed = ProductFormSchema(**form)
            return {
                "success": {
                    "product": parsed.model_dump(exclude_none=True)
                }
            }
        elif form_name == "edit":
            parsed = ProductFormSchema.with_unset(form)
            return {"success": {"product": parsed.model_dump()}}

    except KeyError as e:
        # These shouldn't occur unless middleware or form template is broken
        print("KeyError:", e)
        return {
            "failure": {
                "errors": [{
                    "loc": ["unknown"],
                    "msg": f"Missing field: {str(e)}",
                    "type": "key_error",
                }]
            }
        }

    except (ValueError, ValidationError) as e:
        print("FormError:", e)
        errors = e.errors()
        # field_errors will be passed to the template in context
        field_errors = {}
        flash = []
        for error in errors:
            match error["type"]:
                case "value_error":
                    loc = error.get("loc", [])
                    msg = error.get("msg", "Invalid value.")

                    # if `loc` is not an empty tuple
                    if loc:
                        # iterate over the locations to create `field_errors`
                        for field in loc:
                            # Create the list if it doesn't exist
                            if field not in field_errors:
                                field_errors[field] = []
                            # Add the error message string to the list
                            field_errors[field].append(msg)
                    # if `loc` is an empty tuple
                    else:
                        # set the field name as `__global__`
                        field = "__global__"
                        # Add the error message string to the flash list
                        flash.append(msg)
                case "string_too_short":
                    loc = error.get("loc", [])
                    msg = error.get("msg", "Too short.")

                    # if `loc` is not an empty tuple
                    if loc:
                        # iterate over the locations to create `field_errors`
                        for field in loc:
                            # Create the list if it doesn't exist
                            if field not in field_errors:
                                field_errors[field] = []
                            # Add the error message string to the list
                            field_errors[field].append(msg)
                    # if `loc` is an empty tuple
                    else:
                        # Add the error message string to the flash list
                        flash.append(msg)
                case "string_too_long":
                    loc = error.get("loc", [])
                    msg = error.get("msg", "Too long.")

                    # if `loc` is not an empty tuple
                    if loc:
                        # iterate over the locations to create `field_errors`
                        for field in loc:
                            # Create the list if it doesn't exist
                            if field not in field_errors:
                                field_errors[field] = []
                            # Add the error message string to the list
                            field_errors[field].append(msg)
                    # if `loc` is an empty tuple
                    else:
                        # Add the error message string to the flash list
                        flash.append(msg)
                case "string_pattern_mismatch":
                    loc = error.get("loc", [])
                    msg = error.get("msg", "Invalid pattern.")

                    # if `loc` is not an empty tuple
                    if loc:
                        # iterate over the locations to create `field_errors`
                        for field in loc:
                            # Create the list if it doesn't exist
                            if field not in field_errors:
                                field_errors[field] = []
                            # Add the error message string to the list
                            field_errors[field].append(msg)
                    # if `loc` is an empty tuple
                    else:
                        # Add the error message string to the flash list
                        flash.append(msg)
                case _:
                    raise ValueError(
                        f"-- unhandled error type: {error['type']} --")

        if len(flash) < 1:
            # Add a generic error message string to the flash list
            flash.append("Check the highlighted fields for errors.")

        return {"failure": {"field_errors": field_errors, "flash": flash}}
