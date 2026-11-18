from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models import Usuario, UsuarioApartamento, Apartamento

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

@router.get("/painel")
def painel(request: Request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    db = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        if usuario is None or not usuario.ativo:
            request.session.clear()

            return RedirectResponse(
                url="/login",
                status_code=303
            )

        vinculos = db.query(UsuarioApartamento).filter(
            UsuarioApartamento.usuario_id == usuario.id
        ).all()

        apartamentos = []

        for vinculo in vinculos:
            apartamento = db.query(Apartamento).filter(
                Apartamento.id == vinculo.apartamento_id
            ).first()

            if apartamento is not None:
                apartamentos.append(apartamento)

        return templates.TemplateResponse(
            request=request,
            name="painel.html",
            context={
                "usuario": usuario.nome,
                "apartamentos": apartamentos
            }
        )

    finally:
        db.close()