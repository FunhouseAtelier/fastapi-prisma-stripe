# app/utils/router.py

from typing import Any, Callable

from fastapi import APIRouter as FastAPIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.types import DecoratedCallable


class APIRouter(FastAPIRouter):

    def api_route(self,
                  path: str,
                  *,
                  include_in_schema: bool = True,
                  **kwargs: Any
                  ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        # Normalize the input path
        normalized_path = path.strip("/")  # Handles "", "/", and "/route/"
        path = "/" + normalized_path if normalized_path else ""

        # Compute the full canonical path for analysis
        full_path = self.prefix.rstrip("/") + "/" + path.lstrip("/")
        full_path = full_path.rstrip("/") or "/"

        # Register canonical route (no trailing slash)
        main_route = super().api_route(path,
                                       include_in_schema=include_in_schema,
                                       **kwargs)

        # Add redirect from trailing slash → canonical (unless it's root "/")
        if full_path != "/" and not path.endswith("/"):
            redirect_path = path.rstrip("/") + "/"

            async def redirect_view(request: Request) -> RedirectResponse:
                url = request.url.path.rstrip("/")
                if request.url.query:
                    url += f"?{request.url.query}"
                return RedirectResponse(url, status_code=307)

            super().add_api_route(
                redirect_path,
                endpoint=redirect_view,
                include_in_schema=False,
                methods=kwargs.get("methods", ["GET"]),
            )

        return main_route
