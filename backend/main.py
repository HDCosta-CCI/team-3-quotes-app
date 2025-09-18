from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from middleware.auth_context import AuthContextMiddleware
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router
from routes.quote_routes import router as quotes_router
from models.users import Users
from models.quotes import Quotes
from models.user_quote_reactions import UserQuoteReactions


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthContextMiddleware)

# Include all routes

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(quotes_router)

def custom_openapi():
    # main.py (inside custom_openapi)
    schema = get_openapi(
        title=app.title, version=app.version,
        description=app.description, routes=app.routes
    )

    components = schema.setdefault("components", {})
    schemes = components.setdefault("securitySchemes", {})

    # 🔧 remove any auto-added HTTPBearer schemes
    for key in list(schemes.keys()):
        if key.lower().startswith("httpbearer"):
            del schemes[key]

    # ✅ now add exactly the two you want
    schemes["bearerAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    schemes["refreshAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

    # optional: set a global default (applies to ALL routes)
    schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = schema

    return app.openapi_schema


app.openapi = custom_openapi