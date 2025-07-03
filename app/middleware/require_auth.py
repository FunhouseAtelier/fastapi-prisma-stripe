# app/middleware/require_auth.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.utils.envars import AUTH_STATUS

class AuthRequiredMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        if AUTH_STATUS == "disabled":
            # print("auth disabled")
            return await call_next(request)
        
        path = request.url.path
        session = request.session

        # Allow unauthenticated access to public paths
        public_paths = [
            "/login",
            "/logout",
            "/static",
        ]
        if any(path.startswith(p) for p in public_paths):
            return await call_next(request)

        if not session.get("id58"):
            session["flash"] = ["Please log in to continue."]
            return RedirectResponse("/login", status_code=303)

        return await call_next(request)