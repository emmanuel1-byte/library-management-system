from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from src.modules.auth.route import auth
from src.modules.users.route import user
from src.modules.profile.route import profile
from src.modules.book.route import book
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


@app.get("/", tags=["Health"])
def health_check():
    return JSONResponse(content={"message": "API is running.."}, status_code=200)
