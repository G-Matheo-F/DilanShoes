<<<<<<< HEAD
from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    cantidad: int
=======
from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    nombre: str
    precio: float = Field(40, ge=0, description="El precio debe ser mayor o igual a 0")
    cantidad: int = Field(..., ge=0, description="La cantidad debe ser mayor o igual a 0")
>>>>>>> 994b299 (Sistema DilanShoes|Matheo Flores nivel 6 Analisis y Diseño de Sistemas)
