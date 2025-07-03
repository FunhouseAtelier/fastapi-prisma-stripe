# app/routes/view/client.py

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.utils.db.client import (
  create_client,
  delete_client,
  read_all_clients,
  read_one_client,
  update_client,
)
from app.utils.flash import get_flashes
from app.utils.form import parse_record
from app.utils.format import force_string_to_list
from app.utils.router import APIRouter
from app.utils.security import require_role, get_client_filter, is_admin
from app.utils.templates import render
from app.utils.validators.client import validate_client_form

router = APIRouter(prefix="/client")


@router.get("/")
@require_role(["admin", "sales", "tech"])
async def get_all_clients(request: Request):
    
    where = get_client_filter(request)
    result = await read_all_clients(where)
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    data = result["success"]

    return render(
        "client/all.jinja",
        request,
        {
            "clients": data["clients"],
            "id58_by_id": data["id58_by_id"],
            "flash": get_flashes(request),
        },
    )

@router.get("/new")
@require_role(["admin", "sales"])
async def get_new_client(request: Request):
    return render(
        "client/new.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or {},
            "flash": get_flashes(request),
        },
    )


@router.post("/new")
@require_role(["admin", "sales"])
async def post_new_client(request: Request):

    result = await validate_client_form("new", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "client/new.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    client = result["success"]["client"]

    result = await create_client(client)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "client/new.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    id58 = result["success"]["id58"]

    return RedirectResponse(url=f"/client/{id58}", status_code=303)


@router.get("/{id58}")
@require_role(["admin", "sales", "tech"])
async def get_show_client(request: Request, id58: str):

    result = await read_one_client(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "client/all.jinja",
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
    client = result["success"]["client"]

    if not is_admin(request):
        allowed_ids = set(request.session.get("sales_client_ids", [])) | set(request.session.get("tech_client_ids", []))
        if client.id not in allowed_ids:
            request.session["flash"] = ["You do not have access to that client."]
            return RedirectResponse("/client", status_code=303)

    return render(
        "client/show.jinja",
        request,
        {
            "client": client,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.get("/{id58}/edit")
@require_role(["admin", "sales"])
async def get_edit_client(request: Request, id58: str):

    result = await read_one_client(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "client/edit.jinja",
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
    client = result["success"]["client"]
    id58 = result["success"]["id58"]

    if not is_admin(request):
        allowed_ids = set(request.session.get("sales_client_ids", []))
        if client.id not in allowed_ids:
            request.session["flash"] = ["You do not have access to that client."]
            return RedirectResponse("/client", status_code=303)

    parsed_record = parse_record(client)
    return render(
        "client/edit.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or parsed_record,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.post("/{id58}/edit")
@require_role(["admin", "sales"])
async def post_edit_client(request: Request, id58: str):

    result = await validate_client_form("edit", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "client/edit.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "id58": id58,
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    client = result["success"]["client"]

    if not is_admin(request):
        allowed_ids = set(request.session.get("sales_client_ids", []))
        if client.id not in allowed_ids:
            request.session["flash"] = ["You do not have access to that client."]
            return RedirectResponse("/client", status_code=303)

    result = await update_client(id58, client)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "client/edit.jinja",
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

    return RedirectResponse(url=f"/client/{id58}", status_code=303)


@router.get("/{id58}/delete")
@require_role(["admin"])
async def get_delete_client(request: Request, id58: str):

    result = await read_one_client(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "client/edit.jinja",
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
    client = result["success"]["client"]

    return render(
        "client/delete.jinja",
        request,
        {
            "client": client,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.post("/{id58}/delete")
@require_role("admin")
async def post_delete_client(request: Request, id58: str):

    result = await delete_client(id58)
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

    return RedirectResponse(url="/client", status_code=303)
