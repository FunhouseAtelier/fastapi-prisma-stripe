# app/middleware/form_data.py

from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


def try_parse_date_like_field(field_name: str, value: str):
    """Convert to datetime if field ends in `_at` and parse succeeds."""
    if not isinstance(value, str) or not value.strip():
        return None  # Normalize empty strings to None

    if not field_name.endswith("_at"):
        return value

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return value


class FormDataMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        form = await request.form()
        parsed_form = {}

        for key in form.keys():
            values = form.getlist(key)
            processed = [
                try_parse_date_like_field(key, v)
                for v in values
                if v is not None and v.strip()  # Skip empty
            ]

            if not processed:
                continue  # Don't include key at all if it's empty

            parsed_form[key] = processed if len(processed) > 1 else processed[0]

        request.state.form = parsed_form
        return await call_next(request)
