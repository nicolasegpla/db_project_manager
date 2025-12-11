# app/models/proyecto.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)

    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    empresa = relationship("Empresa", back_populates="proyectos")
    historias_usuario = relationship("HistoriaUsuario", back_populates="proyecto", cascade="all, delete")
