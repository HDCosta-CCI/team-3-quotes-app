# middleware/auth_context.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from auth.token import validate_token

EXCLUDED_PATHS = ["/auth/sign-in", "/auth/sign-up", "/auth/refresh"]

class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
            return await call_next(request)
        
        request.state.auth = None
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            try:
                payload = validate_token(token)
                
                request.state.auth = {
                    "sub": payload.get("first_name"),
                    "user_id": payload.get("user_id"),
                    "email": payload.get("email")
                }
            except JWTError as e:
                
                request.state.auth = None
                request.state.auth_error = str(e)

        response = await call_next(request)
        return response
