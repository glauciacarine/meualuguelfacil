from datetime import date

from sqlalchemy import String, Boolean, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Apartamento(Base):
    __tablename__ = "apartamentos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    numero: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    moradores: Mapped[list["Morador"]] = relationship(
        back_populates="apartamento"
    )

class Morador(Base):
    __tablename__ = "moradores"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    apartamento_id: Mapped[int] = mapped_column(
        ForeignKey("apartamentos.id"),
        nullable=False
    )

    data_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    data_fim: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )   

    apartamento: Mapped["Apartamento"] = relationship(
        back_populates="moradores"
    )

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    administrador: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

class UsuarioApartamento(Base):
    __tablename__ = "usuarios_apartamentos"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        primary_key=True
        )

    apartamento_id: Mapped[int] = mapped_column(
        ForeignKey("apartamentos.id"),
        primary_key=True
        )