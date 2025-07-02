# app/main.py

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.middleware.form_data import FormDataMiddleware
from app.middleware.password_reset_required import PasswordResetRequiredMiddleware
from app.routes.auth import router as auth_router
from app.routes.view.associate import router as associate_view_router
from app.routes.view.client import router as client_view_router
from app.routes.view.order import router as order_view_router
from app.routes.view.product import router as product_view_router
from app.utils.envars import SESSION_SECRET
from app.utils.prisma import connect_prisma, disconnect_prisma
from app.utils.templates import render


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_prisma()
    yield
    await disconnect_prisma()


middleware = [
    Middleware(SessionMiddleware, secret_key=SESSION_SECRET),
    Middleware(FormDataMiddleware),
    Middleware(PasswordResetRequiredMiddleware),
]

app = FastAPI(
    lifespan=lifespan,
    middleware=middleware,
)

# Mount static and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API routes
app.include_router(auth_router)
app.include_router(associate_view_router)
app.include_router(client_view_router)
app.include_router(product_view_router)
app.include_router(order_view_router)


# Homepage (Jinja2 demo)
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return render("home.jinja", request)


# Catch-all route for unmatched paths
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(full_path: str, request: Request):
    print("⚠️ Caught by catch-all route:", full_path)
    if full_path.startswith("api/") or full_path.startswith("static/"):
        raise HTTPException(status_code=404)
    return render("errors/not-found.jinja", request)


# # log all mounted routes
# for route in app.routes:
#     print(f"{route.path} -> {route.name}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)