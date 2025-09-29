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

SETUP_ALLOWED_PATHS = ["/realtor/setup"]

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
            return RedirectResponse(url="/login")
        request.scope["user"] = user

        # Realtor profile completion gate
        try:
            from backend.src.api.realtor_profile import is_realtor_profile_complete
            if user_role == 'realtor' and request.url.path.startswith('/realtor'):
                complete = is_realtor_profile_complete(int(user_id))
                if not complete and all(not request.url.path.startswith(p) for p in SETUP_ALLOWED_PATHS):
                    return RedirectResponse(url="/realtor/setup")
        except Exception:
            pass

        # Check for role-based access to protected routes.
        for path_prefix, required_role in PROTECTED_ROUTES.items():
            if request.url.path.startswith(path_prefix):
                if user_role != required_role:
                    return RedirectResponse(url=f"/{user_role}/dashboard")
                break

        if request.url.path == f"/{user_role}/dashboard":
            return await call_next(request)

        return await call_next(request)
