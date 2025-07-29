from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    nombre: str
    precio: float = Field(40, ge=0, description="El precio debe ser mayor o igual a 0")
    cantidad: int = Field(..., ge=0, description="La cantidad debe ser mayor o igual a 0")
