# app/routes/view/product.py

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.utils.db.product import (
  create_product,
  delete_product,
  read_all_products,
  read_one_product,
  update_product,
)
from app.utils.flash import get_flashes
from app.utils.form import parse_record
from app.utils.format import force_string_to_list
from app.utils.router import APIRouter
from app.utils.templates import render
from app.utils.validators.product import validate_product_form

router = APIRouter(prefix="/product")


@router.get("/")
async def get_all_products(request: Request):

    result = await read_all_products()
    if "failure" in result:
        return render(
            "errors/server-error.jinja", request, {"failure": result["failure"]}
        )
    data = result["success"]

    return render(
        "product/all.jinja",
        request,
        {
            "products": data["products"],
            "id58_by_id": data["id58_by_id"],
            "flash": get_flashes(request),
        },
    )


@router.get("/new")
async def get_new_product(request: Request):
    return render(
        "product/new.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or {},
            "flash": get_flashes(request),
        },
    )


@router.post("/new")
async def post_new_product(request: Request):

    result = await validate_product_form("new", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "product/new.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    product = result["success"]["product"]

    result = await create_product(product)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "product/new.jinja",
                request,
                {
                    "form": getattr(request.state, "form", {}) or {},
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    id58 = result["success"]["id58"]

    return RedirectResponse(url=f"/product/{id58}", status_code=303)


@router.get("/{id58}")
async def get_show_product(request: Request, id58: str):

    result = await read_one_product(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "product/all.jinja",
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
    product = result["success"]["product"]

    return render(
        "product/show.jinja",
        request,
        {
            "product": product,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.get("/{id58}/edit")
async def get_edit_product(request: Request, id58: str):

    result = await read_one_product(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "product/edit.jinja",
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
    product = result["success"]["product"]
    id58 = result["success"]["id58"]

    parsed_record = parse_record(product)
    return render(
        "product/edit.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or parsed_record,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.post("/{id58}/edit")
async def post_edit_product(request: Request, id58: str):

    result = await validate_product_form("edit", request)
    if "failure" in result:
        fail = result["failure"]
        return render(
            "product/edit.jinja",
            request,
            {
                "form": getattr(request.state, "form", {}) or {},
                "id58": id58,
                "field_errors": fail["field_errors"],
                "flash": force_string_to_list(fail["flash"]),
            },
        )
    product = result["success"]["product"]

    result = await update_product(id58, product)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "product/edit.jinja",
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

    return RedirectResponse(url=f"/product/{id58}", status_code=303)


@router.get("/{id58}/delete")
async def get_delete_product(request: Request, id58: str):

    result = await read_one_product(id58)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "product/edit.jinja",
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
    product = result["success"]["product"]

    return render(
        "product/delete.jinja",
        request,
        {
            "product": product,
            "id58": id58,
            "flash": get_flashes(request),
        },
    )


@router.post("/{id58}/delete")
async def post_delete_product(request: Request, id58: str):

    result = await delete_product(id58)
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

    return RedirectResponse(url="/product", status_code=303)
