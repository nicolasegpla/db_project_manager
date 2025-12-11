# app/models/historia_usuario.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.db import Base

class HistoriaUsuario(Base):
    __tablename__ = "historias_usuario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)

    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(50), default="pendiente")
    prioridad = Column(String(50), default="media")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    proyecto = relationship("Proyecto", back_populates="historias_usuario")

    # Correcto: relación con tickets
    tickets = relationship("Ticket", back_populates="historia_usuario", cascade="all, delete")
