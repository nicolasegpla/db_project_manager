from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base


class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    identificacion_tributaria = Column(String(100), unique=True, nullable=False)
    email_contacto = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    telefono_contacto = Column(String(50), nullable=True)
    direccion = Column(String(255), nullable=True)
    pais = Column(String(100), nullable=True)
    ciudad = Column(String(100), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    # --- WhatsApp Cloud API ---
    whatsapp_phone_number_id = Column(String(100), nullable=True)
    whatsapp_business_id = Column(String(100), nullable=True)
    whatsapp_access_token = Column(String(500), nullable=True)
    whatsapp_habilitado = Column(Boolean, default=False)
    whatsapp_conectado_en = Column(DateTime(timezone=True), nullable=True)

    activa = Column(Boolean, default=True)
    creada_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizada_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con usuarios y proyectos
    usuarios = relationship("Usuario", back_populates="empresa", cascade="all, delete")
    proyectos = relationship("Proyecto", back_populates="empresa", cascade="all, delete")

