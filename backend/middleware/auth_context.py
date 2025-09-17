# middleware/auth_context.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from auth.token import validate_token

class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
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
