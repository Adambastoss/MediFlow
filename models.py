from typing import List, Optional

from sqlalchemy import CHAR, Enum, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = 'cliente'
    __table_args__ = (
        Index('CPF', 'CPF', unique=True),
        Index('EMAIL', 'EMAIL', unique=True)
    )

    ID_CLIENTE: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    NOME: Mapped[str] = mapped_column(String(60))
    SEXO: Mapped[str] = mapped_column(Enum('M', 'F'))
    EMAIL: Mapped[Optional[str]] = mapped_column(String(50))
    CPF: Mapped[Optional[str]] = mapped_column(String(16))

    endereco: Mapped[List['Endereco']] = relationship('Endereco', back_populates='cliente')
    telefone: Mapped[List['Telefone']] = relationship('Telefone', back_populates='cliente')


class Endereco(Base):
    __tablename__ = 'endereco'
    __table_args__ = (
        ForeignKeyConstraint(['ID_CLIENTE'], ['cliente.ID_CLIENTE'], name='endereco_ibfk_1'),
        Index('ID_CLIENTE', 'ID_CLIENTE', unique=True)
    )

    ID_ENDERECO: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    BAIRRO: Mapped[str] = mapped_column(String(60))
    RUA: Mapped[str] = mapped_column(String(60))
    NUM: Mapped[int] = mapped_column(INTEGER(11))
    CIDADE: Mapped[str] = mapped_column(String(40))
    UF: Mapped[str] = mapped_column(CHAR(2))
    ID_CLIENTE: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    cliente: Mapped[Optional['Cliente']] = relationship('Cliente', back_populates='endereco')


class Telefone(Base):
    __tablename__ = 'telefone'
    __table_args__ = (
        ForeignKeyConstraint(['ID_CLIENTE'], ['cliente.ID_CLIENTE'], name='telefone_ibfk_1'),
        Index('ID_CLIENTE', 'ID_CLIENTE')
    )

    ID_TELEFONE: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    TIPO: Mapped[str] = mapped_column(Enum('RES', 'COM', 'CEL'))
    DDD: Mapped[str] = mapped_column(String(5))
    NUMERO: Mapped[str] = mapped_column(String(10))
    ID_CLIENTE: Mapped[Optional[int]] = mapped_column(INTEGER(11))

    cliente: Mapped[Optional['Cliente']] = relationship('Cliente', back_populates='telefone')
