from typing import Callable

from backend.src.auth.crud import get_user_by_id
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

# Define routes that are protected and the role required to access them.
# The keys are path prefixes.
PROTECTED_ROUTES = {
    "/admin": "admin",
    "/realtor": "realtor",
    "/client": "client"
}

# Define paths that are publicly accessible and do not require authentication.
PUBLIC_PATHS = [
    "/login", "/register", "/assets", "/favicon.ico",
    "/forgot-password", "/reset-password", "/verify-account"
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Allow public paths
        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            return await call_next(request)

        user_id = request.session.get("user_id")
        user_role = request.session.get("user_role")

        # If no user is logged in, redirect to the login page.
        if not user_id:
            return RedirectResponse(url=f"/login?redirect_to={request.url.path}")

        # Attach the user object to the request scope for easy access in routes.
        user = await get_user_by_id(user_id)
        if not user:
             # Handle case where user in session doesn't exist in DB
            # request.session.clear()
            return RedirectResponse(url="/login")
        request.scope["user"] = user

        # Check for role-based access to protected routes.
        for path_prefix, required_role in PROTECTED_ROUTES.items():
            if request.url.path.startswith(path_prefix):
                if user_role != required_role:
                    # If the user has the wrong role, deny access by redirecting.
                    return RedirectResponse(url=f"/{user_role}/dashboard")
                # If the role is correct, break the loop and proceed.
                break

        # If user is trying to access their own dashboard, let them through.
        if request.url.path == f"/{user_role}/dashboard":
            return await call_next(request)

        return await call_next(request)
