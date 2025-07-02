# app/routes/view/order.py

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.utils.db.associate import read_all_associates
from app.utils.db.client import read_all_clients
from app.utils.db.order import (
  create_order,
  delete_order,
  read_all_orders,
  read_one_order,
  update_order,
)
from app.utils.flash import get_flashes
from app.utils.form import parse_record
from app.utils.format import force_string_to_list
from app.utils.router import APIRouter
from app.utils.security import require_role
from app.utils.templates import render
from app.utils.validators.order import validate_order_form

router = APIRouter(prefix="/order")


@router.get("/")
@require_role(["admin", "sales", "tech"])
async def get_all_orders(request: Request):

    result = await read_all_orders()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    data = result["success"]

    return render(
        "order/all.jinja",
        request,
        {
            "orders": data["orders"],
            "id58_by_id": data["id58_by_id"],
            "flash": get_flashes(request),
        },
    )


@router.get("/new")
@require_role(["admin", "sales"])
async def get_new_order(request: Request):

    result = await read_all_associates()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    associates = result["success"]["associates"]

    result = await read_all_clients()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    clients = result["success"]["clients"]

    return render(
        "order/new.jinja",
        request,
        {
            "clients": clients,
            "associates": associates,
            "form": getattr(request.state, "form", {}) or {},
            "flash": get_flashes(request),
        },
    )


@router.post("/new")
@require_role(["admin", "sales"])
async def post_new_order(request: Request):

    result = await validate_order_form("new", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "order/new.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    order = result["success"]["order"]

    result = await create_order(order)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "order/new.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": force_string_to_list(force_string_to_list(fail["msg"])),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    id58 = result["success"]["id58"]

    return RedirectResponse(url=f"/order/{id58}", status_code=303)


@router.get("/{id58}")
@require_role(["admin", "sales", "tech"])
async def get_show_order(request: Request, id58: str):

    result = await read_one_order(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "order/all.jinja",
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
    order = result["success"]["order"]

    return render(
        "order/show.jinja",
        request,
        {
            "order": order,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.get("/{id58}/edit")
@require_role(["admin", "sales"])
async def get_edit_order(request: Request, id58: str):

    result = await read_one_order(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "order/edit.jinja",
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
    order = result["success"]["order"]
    id58 = result["success"]["id58"]

    result = await read_all_associates()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    associates = result["success"]["associates"]

    result = await read_all_clients()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    clients = result["success"]["clients"]

    parsed_record = parse_record(order)
    return render(
        "order/edit.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or parsed_record,
            "id58": id58,
            "flash": get_flashes(request),
            "associates": associates,
            "clients": clients,
        },
    )


@router.post("/{id58}/edit")
@require_role(["admin", "sales"])
async def post_edit_order(request: Request, id58: str):

    result = await validate_order_form("edit", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "order/edit.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "id58": id58,
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    order = result["success"]["order"]

    result = await update_order(id58, order)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "order/edit.jinja",
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

    return RedirectResponse(url=f"/order/{id58}", status_code=303)


@router.get("/{id58}/delete")
@require_role(["admin", "sales"])
async def get_delete_order(request: Request, id58: str):

    result = await read_one_order(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "order/edit.jinja",
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
    order = result["success"]["order"]

    return render(
        "order/delete.jinja",
        request,
        {
            "order": order,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.post("/{id58}/delete")
@require_role(["admin", "sales"])
async def post_delete_order(request: Request, id58: str):

    result = await delete_order(id58)
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

    return RedirectResponse(url="/order", status_code=303)
