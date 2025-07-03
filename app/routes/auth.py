# app/routes/auth.py

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from app.utils.db.associate import get_associate_by_username, update_associate
from app.utils.flash import get_flashes
from app.utils.format import force_string_to_list, encode_id
from app.utils.security import verify_password, generate_salt, hash_password
from app.utils.session import create_session, force_password_reset_required, clear_session
from app.utils.templates import render

router = APIRouter()

@router.get("/login")
async def get_login(request: Request):
    if request.session.get("id58"):
        return RedirectResponse("/", status_code=303)
    # Clear any existing session (optional: avoids stale login)
    clear_session(request)
    return render(
        "login.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or {},
            "flash": get_flashes(request),
        },
    )

@router.post("/login")
async def post_login(request: Request):

    form = getattr(request.state, "form", {}) or {}
    username = form.get("username")
    password = form.get("password")
    
    if not username or not password:
      return render(
        "login.jinja",
        request,
        {
          "form": form,
          "flash": force_string_to_list("Username and password are required."),
        },
      )

    result = await get_associate_by_username(username)
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "login.jinja",
                request,
                {
                    "form": form,
                    "flash": force_string_to_list(fail["msg"]),
                },
            )
        elif fail["type"] == "not_found":
            return render(
                "login.jinja",
                request,
                {
                    "form": form,
                    "flash": force_string_to_list("Invalid credentials."),
                },
            )
        return render("errors/server-error.jinja", request, {"failure": fail})
    associate = result["success"]["associate"]

    if not associate or associate.locked_at is not None:
        return render(
            "login.jinja",
            request,
            {
                "form": form,
                "flash": force_string_to_list("Invalid credentials."),
            },
        )

    if associate.password is None:
        # First login: using temporary password (first 12 of salt)
        if password != associate.salt[:12]:
            return render(
                "login.jinja",
                request,
                {
                    "form": form,
                    "flash": force_string_to_list("Invalid temporary password."),
                },
            )

        # Valid temp login — must set password
        id58 = result["success"]["id58"]
        await create_session(request, id58)
        force_password_reset_required(request)
        return RedirectResponse("/auth/set-password", status_code=303)

    # Regular login flow
    if not verify_password(password, associate.password, associate.salt):
        request.session["flash"] = ["Invalid credentials."]
        return render(
            "login.jinja",
            request,
            {
                "form": form,
                "flash": force_string_to_list("Invalid credentials."),
            },
        )

    id58 = result["success"]["id58"]
    await create_session(request, id58)
    return RedirectResponse("/", status_code=303)

@router.get("/auth/set-password")
async def get_set_password(request: Request):
    
    if not request.session.get("id58"):
        return RedirectResponse("/login", status_code=303)
    
    return render(
        "set-password.jinja",
        request,
        {
            "form": getattr(request.state, "form", {}) or {},
            "flash": get_flashes(request),
        },
    )

@router.post("/auth/set-password")
async def post_set_password(request: Request):
    
    form = getattr(request.state, "form", {}) or {}
    password = form.get("password")
    confirm = form.get("confirm")

    if not password or not confirm:
        return render("set-password.jinja", request, {
            "form": form,
            "flash": ["All fields are required."]
        })

    if password != confirm:
        return render("set-password.jinja", request, {
            "form": form,
            "flash": ["Passwords do not match."]
        })

    if len(password) < 8:
        return render("set-password.jinja", request, {
            "form": form,
            "flash": ["Password must be at least 8 characters."]
        })

    id58 = request.session.get("id58")
    if not id58:
        request.session["flash"] = ["Invalid session."]
        return RedirectResponse("/login", status_code=303)

    new_salt = generate_salt()
    new_hash = hash_password(password, new_salt)

    result = await update_associate(id58, {
        "password": new_hash,
        "salt": new_salt
    })
    if "failure" in result:
        fail = result["failure"]
        if fail["type"] == "db":
            return render(
                "set-password.jinja",
                request,
                {
                    "form": form,
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
    
    # Clear reset flag
    request.session.pop("must_reset_password", None)
    request.session["flash"] = ["Password updated successfully!"]
    return RedirectResponse("/", status_code=303)

@router.get("/logout")
async def get_logout(request: Request):
  clear_session(request)
  request.session["flash"] = ["You are now logged out."]
  return RedirectResponse("/login", status_code=303)
