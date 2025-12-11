# app/models/ticket.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    historia_usuario_id = Column(Integer, ForeignKey("historias_usuario.id", ondelete="CASCADE"), nullable=False)

    asunto = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(50), default="abierto")
    prioridad = Column(String(50), default="media")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relación correcta con historia_usuario
    historia_usuario = relationship("HistoriaUsuario", back_populates="tickets")
