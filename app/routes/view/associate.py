# app/routes/view/associate.py

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.utils.db.associate import (
  create_associate,
  delete_associate,
  read_all_associates,
  read_one_associate,
  update_associate,
)
from app.utils.flash import get_flashes
from app.utils.form import parse_record
from app.utils.format import force_string_to_list
from app.utils.router import APIRouter
from app.utils.security import require_role
from app.utils.templates import render
from app.utils.validators.associate import validate_associate_form

router = APIRouter(prefix="/associate")

@router.get("/")
@require_role("admin")
async def get_all_associates(request: Request):
    
    result = await read_all_associates()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    data = result["success"]

    return render(
        "associate/all.jinja",
        request,
        {
            "associates": data["associates"],
            "id58_by_id": data["id58_by_id"],
            "flash": get_flashes(request),
        },
    )


@router.get("/new")
@require_role("admin")
async def get_new_associate(request: Request):
    
   
    return render(
        "associate/new.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or {},
            "flash": get_flashes(request),
        },
    )


@router.post("/new")
@require_role("admin")
async def post_new_associate(request: Request):
    
    result = await validate_associate_form("new", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "associate/new.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    associate = result["success"]["associate"]

    result = await create_associate(associate)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "associate/new.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    id58 = result["success"]["id58"]

    return RedirectResponse(url=f"/associate/{id58}", status_code=303)


@router.get("/{id58}")
@require_role("admin")
async def get_show_associate(request: Request, id58: str):
    
    result = await read_one_associate(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "associate/all.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        elif fail["type"] == "not_found":
            return render(
                "errors/not-found.jinja",
                request,
                {
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    associate = result["success"]["associate"]

    return render(
        "associate/show.jinja",
        request,
        {
            "associate": associate,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.get("/{id58}/edit")
@require_role("admin")
async def get_edit_associate(request: Request, id58: str):
    
    result = await read_one_associate(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "associate/edit.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        elif fail["type"] == "not_found":
            return render(
                "errors/not-found.jinja",
                request,
                {
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    associate = result["success"]["associate"]
    id58 = result["success"]["id58"]

    parsed_record = parse_record(associate)
    return render(
        "associate/edit.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or parsed_record,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.post("/{id58}/edit")
@require_role("admin")
async def post_edit_associate(request: Request, id58: str):
    
    result = await validate_associate_form("edit", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "associate/edit.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "id58": id58,
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    associate = result["success"]["associate"]

    result = await update_associate(id58, associate)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "associate/edit.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "id58": id58,
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        elif fail["type"] == "not_found":
            return render(
                "errors/not-found.jinja",
                request,
                {
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    id58 = result["success"]["id58"]

    return RedirectResponse(url=f"/associate/{id58}", status_code=303)


@router.get("/{id58}/delete")
@require_role("admin")
async def get_delete_associate(request: Request, id58: str):
    
    result = await read_one_associate(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "associate/edit.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": fail["msg"],
                },
            )
        elif fail["type"] == "not_found":
            return render(
                "errors/not-found.jinja",
                request,
                {
                    "flash": fail["msg"],
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    associate = result["success"]["associate"]

    return render(
        "associate/delete.jinja",
        request,
        {
            "associate": associate,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )

@router.post("/{id58}/delete")
@require_role("admin")
async def post_delete_associate(request: Request, id58: str):
    
    result = await delete_associate(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "errors/server-error.jinja",
                request,
                {"failure": fail},
            )
        elif fail["type"] == "not_found":
            return render(
                "errors/not-found.jinja",
                request,
                {
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})

    return RedirectResponse(url="/associate", status_code=303)
