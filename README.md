Dilan Shoes - Sistema de Gestión de Inventario y Ventas

Este proyecto es un sistema informático para la gestión de inventario y ventas de la tienda Dilan Shoes. Está desarrollado con FastAPI, SQLAlchemy y plantillas Jinja2, además de usar PostgreSQL como base de datos. Cuenta con autenticación, gestión de productos, registro y confirmación de ventas, y una sección para mostrar productos populares.

Tecnologías usadas:
- Python 3.10+
- FastAPI
- SQLAlchemy
- Jinja2 Templates
- PostgreSQL
- Docker (para despliegue y pruebas)
- JavaScript (frontend básico)

Funcionalidades principales:
- Registro y autenticación de usuario.
- CRUD (Crear, Leer, Actualizar, Eliminar) productos en inventario.
- Control de stock y ventas con actualización automática.
- Visualización de productos populares según ventas.
- Manejo de imágenes estáticas para productos.
- Validaciones para stock y cantidades.

Instalación y despliegue:

1. Clonar el repositorio:
   git clone https://github.com/G-Matheo-F/DilanShoes.git
   cd DilanShoes

2. Crear y activar un entorno virtual:
   python -m venv venv
   source venv/bin/activate  (Linux/Mac)
   venv\Scripts\activate     (Windows)

3. Instalar dependencias:
   pip install -r requirements.txt

4. Configurar base de datos PostgreSQL y variables de entorno según app/database.py.

5. Ejecutar migraciones o crear base de datos (según instrucciones internas).

6. Levantar la aplicación:
   uvicorn app.main:app --reload

7. Acceder en el navegador a http://localhost:8000

Estructura del proyecto:

app/
  main.py             - Punto de entrada y rutas principales
  models.py           - Modelos ORM SQLAlchemy
  database.py         - Configuración base de datos y sesión
  templates/          - Plantillas HTML Jinja2
  static/             - Archivos estáticos (css, js, imágenes)
  utils.py            - Funciones utilitarias (auth, seguridad)
  data_default.py     - Inserción inicial de datos quemados

Link al proyecto:
https://github.com/G-Matheo-F/DilanShoes

Autor:
Gerson Matheo Flores Chamorro
