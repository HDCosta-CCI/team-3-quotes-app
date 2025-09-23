from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

def custom_key_func(request: Request):
    
    auth_header = request.headers.get("Authorization")
    print(auth_header)
    if auth_header and auth_header.startswith("Bearer "):
        return None
    
    return get_remote_address(request)

limiter = Limiter(key_func=custom_key_func)
