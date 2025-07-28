from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    ventas = relationship("Venta", back_populates="producto")

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    fecha = Column(DateTime, default=datetime.utcnow)
    producto = relationship("Producto", back_populates="ventas")

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
