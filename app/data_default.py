from sqlalchemy.orm import Session
from app.models import Producto, Venta
from app.database import SessionLocal

def insertar_producto_base():
    db: Session = SessionLocal()
    producto_existente = db.query(Producto).filter_by(id=1).first()

    if not producto_existente:
        nuevo_producto = Producto(
            id=1,
            nombre="Skechers GOwalk Joy",
            precio=65.0,
            cantidad=12
        )
        db.add(nuevo_producto)
        db.commit()
        print("Producto 'Skechers GOwalk Joy' insertado en la base de datos.")
    else:
        print("El producto con id=1 ya existe en la base de datos.")
    db.close()

def insertar_ventas_base():
    db: Session = SessionLocal()
    venta_existente = db.query(Venta).filter_by(producto_id=1).first()

    if not venta_existente:
        # Insertamos 5 ventas de 5 unidades cada una, total 25 ventas
        ventas = [Venta(producto_id=1, cantidad=5) for _ in range(5)]
        db.add_all(ventas)
        db.commit()
        print("Ventas base insertadas en la base de datos.")
    else:
        print("Ya existen ventas para el producto con id=1.")
    db.close()
