# app/utils/templates.py

from datetime import datetime
from pathlib import Path
from typing import Final, Optional

from fastapi import Request
from starlette.templating import Jinja2Templates
from starlette.templating import (
    _TemplateResponse as
    TemplateResponse,  # <-- Note: using starlette directly
)

from app.utils.flash import get_flashes

TEMPLATES_DIR: Final[str] = Path(
    __file__).resolve().parent.parent / "templates"

templates: Final[Jinja2Templates] = Jinja2Templates(directory=TEMPLATES_DIR)

def format_price(cents) -> str:
  return f"${cents / 100:.2f}"
templates.env.filters["format_price"] = format_price

def format_pct(cents) -> str:
  return f"{cents / 100:.2f}%"
templates.env.filters["format_pct"] = format_pct

def format_2f(value) -> str:
  try:
    # Allow string or int input
    cents = int(value)
  except (ValueError, TypeError):
    cents = 0
  return f"{cents / 100:.2f}"
templates.env.filters["format_2f"] = format_2f

def format_date(value) -> str:
  return value.strftime('%Y-%m-%d')
templates.env.filters["format_date"] = format_date

def render(template_name: str,
           request: Request,
           extra_context: Optional[dict] = None) -> TemplateResponse:
    """
    Render a Jinja2 template. Extra variables can be passed via the `extra_context` dictionary.
    """
    context = {
        "request": request,
        "now": datetime.now().timestamp(),
        "flash": get_flashes(request),
    }

    if extra_context:
        context.update(extra_context)

    return templates.TemplateResponse(template_name, context)