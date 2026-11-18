import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.routes.auth import router as auth_router
from app.routes.painel import router as painel_router

from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app import models

app = FastAPI(
    title="Meu Aluguel Fácil",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "chave-apenas-para-desenvolvimento"),
    https_only=False
)

app.include_router(auth_router)
app.include_router(painel_router)

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
        "titulo": "Meu Aluguel Fácil"
    },
    )