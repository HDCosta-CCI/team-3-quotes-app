from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from middleware.auth_context import AuthContextMiddleware
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router
from routes.quote_routes import router as quotes_router
from routes.authors_routes import router as author_router
from models.users import Users
from models.quotes import Quotes
from models.user_quote_reactions import UserQuoteReactions
from dto.response_dto import GlobalResponse

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

# Include all routes
app.include_router(auth_router)
app.add_middleware(AuthContextMiddleware)
app.include_router(user_router)
app.include_router(quotes_router)
app.include_router(author_router)


def custom_openapi():
    schema = get_openapi(
        title=app.title, version=app.version,
        description=app.description, routes=app.routes
    )
    components = schema.setdefault("components", {})
    schemes = components.setdefault("securitySchemes", {})

    for key in list(schemes.keys()):
        if key.lower().startswith("httpbearer"):
            del schemes[key]

    schemes["bearerAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    schemes["refreshAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi

def _dto(message: str, data=None, errors=None) -> dict:
    return GlobalResponse(success=False, message=message, data=data, errors=errors).model_dump()
 
@app.exception_handler(HTTPException)
async def fastapi_http_exception_handler(_, exc: HTTPException):
    msg = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=exc.status_code,
        content= _dto(
            message=msg,
            data=None,
            errors=[{"field": "non_field_errors", "message": str(exc.detail)}],
        )
    )

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(_, exc: StarletteHTTPException):
    msg = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=exc.status_code,
        content= _dto(
            message=msg,
            data=None,
            errors=[{"field": "non_field_errors", "message": str(exc.detail)}],
        )
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    errs = [{"field": ".".join(map(str, e["loc"])), "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content= _dto(message="Validation failed", data=None, errors=errs),
    )