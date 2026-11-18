from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database import SessionLocal
from app.models import Usuario
from app.security import verificar_senha


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "erro": None
        }
    )

@router.post("/login")
def fazer_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...)
):
    db = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.email == email
        ).first()

        if usuario is None:
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "erro": "E-mail ou senha inválidos."
                },
                status_code=401
            )

        if not verificar_senha(
            senha,
            usuario.senha_hash
        ):
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "erro": "E-mail ou senha inválidos."
                },
                status_code=401
            )

        if not usuario.ativo:
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "erro": "Usuário inativo."
                },
                status_code=403
            )

        request.session["usuario_id"] = usuario.id

        return RedirectResponse(
            url="/painel",
            status_code=303
        )

    finally:
        db.close()

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )