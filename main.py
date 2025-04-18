from fastapi import FastAPI
from internal import admin_router, auth_router
from routers import pets_router
from contextlib import asynccontextmanager
from db import create_schema, db_engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_schema(db_engine, Base.metadata)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(pets_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
