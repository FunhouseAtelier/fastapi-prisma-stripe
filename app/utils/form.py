# app/utils/form.py

from typing import Any

from app.middleware.form_data import try_parse_date_like_field


def parse_record(record: Any) -> dict[str, Any]:
    """
    Convert a Pydantic model (e.g. Prisma `Associate`) to dict format
    compatible with `FormDataMiddleware` for use in form components.
    """
    if hasattr(record, "model_dump"):
        record = record.model_dump()

    parsed_form = {}

    for key, value in record.items():
        # Skip nulls or empty strings
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue

        if isinstance(value, list):
            cleaned_list = [
                try_parse_date_like_field(key, str(v)) for v in value
                if str(v).strip()
            ]
            if cleaned_list:
                parsed_form[key] = cleaned_list
        else:
            parsed_form[key] = try_parse_date_like_field(key, str(value))

    return parsed_form
