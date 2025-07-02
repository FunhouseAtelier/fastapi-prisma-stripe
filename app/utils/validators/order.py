# app/utils/validators/order.py

from decimal import Decimal, InvalidOperation
from typing import List, Optional

from fastapi import Request
from pydantic import BaseModel, ValidationError, field_validator

from app.schemas.order import (
    AssociateIdStr,
    AuditedAtDate,
    AuditNotesStr,
    ClientIdStr,
    OrderStatusStr,
    SalesTaxInt,
)
from app.utils.validators.fields import (
    coerce_one_string_to_list,
    trim_one_string,
    unset_if_empty,
)


class OrderFormSchema(BaseModel):
    status: OrderStatusStr
    audited_by_id: Optional[AssociateIdStr] = None
    audit_notes: Optional[AuditNotesStr] = None
    audited_at: Optional[AuditedAtDate] = None
    client_id: ClientIdStr
    sales_tax: SalesTaxInt
    sales_associate_ids: List[AssociateIdStr]
    tech_associate_ids: List[AssociateIdStr]

    # Trim all incoming string fields
    @field_validator("*", mode="before")
    @classmethod
    def trim_string(cls, v):
        return trim_one_string(v)

    @field_validator("audited_by_id",
                     "audit_notes",
                     "audited_at",
                     mode="before")
    @classmethod
    def coerce_empty_strings_to_none(cls, v):
        if v == "":
            return None
        return v

    # Coerce `sales_tax` to int if needed
    @field_validator("sales_tax", mode="before")
    @classmethod
    def coerce_sales_tax(cls, v):
        try:
            if isinstance(v, str):
                # Normalize string input like "19.99"
                return int(Decimal(v) * 100)
            if isinstance(v, (float, Decimal)):
                return int(Decimal(v) * 100)
            if isinstance(v, int):
                return v  # already in cents
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid sales tax format")
        raise ValueError("Invalid sales tax format")

    # Coerce string to list for multi-select fields
    @field_validator("sales_associate_ids",
                     "tech_associate_ids",
                     mode="before")
    @classmethod
    def coerce_associate_ids(cls, v):
        return coerce_one_string_to_list(v)

    @classmethod
    def with_unset(cls, data: dict):
        """Call this to apply `unset_if_empty` logic only for edit forms."""
        fields_to_check = ["ssn", "tin", "business_name", "street_address_2"]
        return cls(
            **{
                k: unset_if_empty(v) if k in fields_to_check else v
                for k, v in data.items()
            })


#
# USE IN ROUTE HANDLERS
#
async def validate_order_form(form_name: str, request: Request) -> dict:
    form = request.state.form
    try:
        if form_name == "new":
            parsed = OrderFormSchema(**form)
            return {"success": {"order": parsed.model_dump(exclude_none=True)}}
        elif form_name == "edit":
            parsed = OrderFormSchema.with_unset(form)
            return {"success": {"order": parsed.model_dump()}}

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
                    flash.append(
                        f"-- unhandled error type: {error['type']} --\n{error}"
                    )
                    print(f"-- unhandled error type: {error['type']} --")

        if len(flash) < 1:
            # Add a generic error message string to the flash list
            flash.append("Check the highlighted fields for errors.")

        return {"failure": {"field_errors": field_errors, "flash": flash}}
