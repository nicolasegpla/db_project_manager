from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base


class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email_contacto = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now()) 
    tipo_suscripcion = Column(String(50), default="basic")
    roll = Column(String(50), default="superUser")

    activa = Column(Boolean, default=True)
    creada_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizada_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con usuarios y proyectos
    usuarios = relationship("Usuario", back_populates="empresa", cascade="all, delete")
    proyectos = relationship("Proyecto", back_populates="empresa", cascade="all, delete")

