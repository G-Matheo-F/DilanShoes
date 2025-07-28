from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Body, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine, Base, get_db
from app.models import Producto, Venta, User
from app.utils import create_user_if_needed, verify_password, create_access_token, get_current_user, get_token_from_cookie
import shutil
import os
from app.data_default import  insertar_producto_base, insertar_ventas_base


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Montar carpeta estática para servir imágenes y otros archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)

# data_deafault.py
@app.on_event("startup")
def startup():
    db = next(get_db())
    create_user_if_needed(db)
    insertar_producto_base()   # Inserta producto quemado si no existe
    insertar_ventas_base()   # Inserta ventas quemadas si no existen

@app.on_event("startup")
def startup():
    db = next(get_db())
    create_user_if_needed(db)

@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Credenciales inválidas"})
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse("/home", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response

@app.get("/home", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)):
    current_user = get_current_user(token=token, db=db)
    return templates.TemplateResponse("home.html", {"request": request, "usuario": current_user.username})

# --- Inventario ---

@app.get("/inventario", response_class=HTMLResponse)
def inventario(request: Request, db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)):
    current_user = get_current_user(token=token, db=db)
    productos = db.query(Producto).all()
    return templates.TemplateResponse("inventario.html", {"request": request, "productos": productos})


@app.post("/productos/agregar")
def agregar_producto(
    nombre: str = Form(...), 
    precio: float = Form(...), 
    cantidad: int = Form(...),
    db: Session = Depends(get_db), 
    token: str = Depends(get_token_from_cookie)
):
    current_user = get_current_user(token=token, db=db)
    producto_existente = db.query(Producto).filter(Producto.nombre == nombre).first()
    if producto_existente:
        producto_existente.cantidad += cantidad

    else:
        nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
        db.add(nuevo)
    db.commit()
    return RedirectResponse("/inventario", status_code=303)


@app.post("/productos/actualizar/{producto_id}")
def actualizar_producto(
    producto_id: int,
    nombre: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_cookie)
):
    current_user = get_current_user(token=token, db=db)
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.nombre = nombre
    producto.precio = precio
    producto.cantidad = stock
    db.commit()
    return RedirectResponse(url="/inventario", status_code=303)


@app.post("/productos/eliminar/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)):
    current_user = get_current_user(token=token, db=db)
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return RedirectResponse("/inventario", status_code=303)


# --- Ventas ---

@app.get("/ventas", response_class=HTMLResponse)
def ventas(request: Request, db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)):
    current_user = get_current_user(token=token, db=db)
    productos = db.query(Producto).filter(Producto.cantidad > 0).all()
    return templates.TemplateResponse("ventas.html", {"request": request, "productos": productos})

@app.post("/ventas/confirmar")
def confirmar_venta(items: dict = Body(...), db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)):
    current_user = get_current_user(token=token, db=db)
    venta_items = items.get("items", [])
    if not venta_items:
        raise HTTPException(status_code=400, detail="No hay productos en la venta")

    # Validar stock
    for item in venta_items:
        producto = db.query(Producto).filter(Producto.id == item["id"]).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {item['nombre']} no encontrado")
        if producto.cantidad < item["cantidad"]:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre}")

    # Reducir stock y registrar venta
    for item in venta_items:
        producto = db.query(Producto).filter(Producto.id == item["id"]).first()
        producto.cantidad -= item["cantidad"]
        venta = Venta(producto_id=producto.id, cantidad=item["cantidad"])
        db.add(venta)

    db.commit()
    return JSONResponse(content={"msg": "Venta confirmada"})

# --- Populares (acceso público) ---

@app.get("/populares", response_class=HTMLResponse)
def ver_populares(request: Request, db: Session = Depends(get_db)):
    populares = (
        db.query(
            Producto,
            func.sum(Venta.cantidad).label("total_vendido")
        )
        .join(Venta, Producto.id == Venta.producto_id)
        .group_by(Producto.id)
        .order_by(func.sum(Venta.cantidad).desc())
        .limit(5)
        .all()
    )
    productos_con_ventas = [{"producto": p[0], "total_vendido": p[1]} for p in populares]
    return templates.TemplateResponse("populares.html", {"request": request, "productos": productos_con_ventas})
