from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from src.modules.auth.route import auth
from src.modules.users.route import user
from src.modules.profile.route import profile
from src.modules.book.route import book
from src.modules.transaction.route import transaction
from src.utils.database import create_table
from src import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth)
app.include_router(user)
app.include_router(profile)
app.include_router(book)
app.include_router(transaction)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="LMS",
        version="1.0.0",
        summary="This is Library Mangement API service",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/", tags=["Health"])
def health_check():
    return JSONResponse(content={"message": "API is running.."}, status_code=200)
