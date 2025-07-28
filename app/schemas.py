from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    cantidad: int
