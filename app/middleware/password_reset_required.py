# app/middleware/password_reset_required.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

class PasswordResetRequiredMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session = request.session
        must_reset = session.get("must_reset_password")
        associate_id = session.get("associate_id")

        exempt_paths = {
            "/auth/set-password",
            "/logout",
            "/static",  # exclude static assets
            "/login"
        }

        # Allow if not logged in or no reset needed
        if not associate_id or not must_reset:
            return await call_next(request)

        # Allow if current path is exempt (exact or prefix match)
        path = request.url.path
        if any(path.startswith(exempt) for exempt in exempt_paths):
            return await call_next(request)

        # Redirect to password reset
        return RedirectResponse("/auth/set-password", status_code=303)
