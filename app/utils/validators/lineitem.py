# app/utils/validators/lineitem.py

from typing import Optional

from fastapi import Request
from pydantic import BaseModel, ValidationError, field_validator, model_validator

from app.schemas.lineitem import (
    BusinessNameStr,
    CityStr,
    EmailAddrStr,
    FullNameStr,
    PhoneNumberStr,
    RolesList,
    SSNStr,
    StreetStr,
    TINStr,
    UsernameStr,
    USStateStr,
    W9Date,
    ZipCodeStr,
)
from app.utils.validators.fields import (
    coerce_one_string_to_list,
    format_one_phone_number,
    format_one_ssn,
    format_one_tin,
    make_one_string_lowercase,
    require_one_field,
    trim_one_string,
    unset_if_empty,
)


class LineitemFormSchema(BaseModel):
    name: FullNameStr
    business_name: Optional[BusinessNameStr] = None
    street_address_1: StreetStr
    street_address_2: Optional[StreetStr] = None
    city: CityStr
    state: USStateStr
    zip_code: ZipCodeStr
    phone: PhoneNumberStr
    email: EmailAddrStr
    username: UsernameStr
    w9_updated_at: W9Date
    ssn: Optional[SSNStr] = None
    tin: Optional[TINStr] = None
    roles: RolesList = []

    @field_validator("*", mode="before")
    @classmethod
    def trim_string(cls, v):
        return trim_one_string(v)

    @field_validator("phone", mode="before")
    @classmethod
    def format_phone(cls, v):
        return format_one_phone_number(v)

    @field_validator("email", "username", mode="before")
    @classmethod
    def make_lowercase(cls, v):
        return make_one_string_lowercase(v)

    @field_validator("ssn", mode="before")
    @classmethod
    def format_ssn(cls, v):
        return format_one_ssn(v)

    @field_validator("tin", mode="before")
    @classmethod
    def format_tin(cls, v):
        return format_one_tin(v)

    @field_validator("roles", mode="before")
    @classmethod
    def coerce_to_list(cls, v):
        return coerce_one_string_to_list(v)

    @model_validator(mode="after")
    def validate_either_ssn_or_tin(self):
        if require_one_field(self, ["ssn", "tin"]):
            return self
        raise ValidationError("Either SSN or TIN must be provided.")

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
async def validate_lineitem_form(form_name: str, request: Request) -> dict:
    form = request.state.form
    try:
        if form_name == "new":
            parsed = LineitemFormSchema(**form)
            return {
                "success": {
                    "lineitem": parsed.model_dump(exclude_none=True)
                }
            }
        elif form_name == "edit":
            parsed = LineitemFormSchema.with_unset(form)
            return {"success": {"lineitem": parsed.model_dump()}}

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
