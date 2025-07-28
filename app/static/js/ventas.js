document.addEventListener('DOMContentLoaded', function() {
    const productosSelect = document.getElementById('producto');
    const cantidadInput = document.getElementById('cantidad');
    const btnAgregar = document.getElementById('btn-agregar');
    const tablaFacturaBody = document.querySelector('#tabla-factura tbody');
    const totalDisplay = document.getElementById('total');
    const btnConfirmar = document.getElementById('btn-confirmar');
    const imagenProducto = document.getElementById('imagen-producto');
    const idProductoSeleccionado = document.getElementById('id-producto-seleccionado');

    let factura = [];

    function actualizarTabla() {
      tablaFacturaBody.innerHTML = '';
      let total = 0;

      factura.forEach((item, index) => {
        const subtotal = item.cantidad * item.precio;
        total += subtotal;

        const tr = document.createElement('tr');

        tr.innerHTML = `
          <td>${item.nombre}</td>
          <td>${item.cantidad}</td>
          <td>$${item.precio.toFixed(2)}</td>
          <td>$${subtotal.toFixed(2)}</td>
          <td><button data-index="${index}" class="btn-eliminar">Eliminar</button></td>
        `;

        tablaFacturaBody.appendChild(tr);
      });

      totalDisplay.textContent = `$${total.toFixed(2)}`;
      btnConfirmar.disabled = factura.length === 0;
    }

    productosSelect.addEventListener('change', () => {
      const productoId = productosSelect.value;
      if(!productoId) {
        imagenProducto.src = "/static/images/default-product.png";
        idProductoSeleccionado.textContent = "ID del producto: -";
        return;
      }
      // Actualizar la imagen según el id seleccionado
      imagenProducto.src = `/static/images/${productoId}.jpg`;
      imagenProducto.onerror = () => {
        imagenProducto.src = "/static/images/default-product.png";
      };

      // Mostrar la ID seleccionada
      idProductoSeleccionado.textContent = `ID del producto: ${productoId}`;
    });

    btnAgregar.addEventListener('click', () => {
      const productoId = productosSelect.value;
      const cantidad = parseInt(cantidadInput.value);

      if (!productoId) {
        alert("Seleccione un producto");
        return;
      }

      if (isNaN(cantidad) || cantidad < 1) {
        alert("Ingrese una cantidad válida");
        return;
      }

      const option = productosSelect.options[productosSelect.selectedIndex];
      const nombre = option.text.split(" - Precio")[0];
      const stock = parseInt(option.getAttribute('data-cantidad'));
      const precio = parseFloat(option.getAttribute('data-precio'));

      let cantidadEnFactura = 0;
      const indexExistente = factura.findIndex(item => item.id === productoId);
      if(indexExistente !== -1) {
        cantidadEnFactura = factura[indexExistente].cantidad;
      }

      if (cantidad + cantidadEnFactura > stock) {
        alert(`No hay suficiente stock. Disponible: ${stock - cantidadEnFactura}`);
        return;
      }

      if(indexExistente !== -1) {
        factura[indexExistente].cantidad += cantidad;
      } else {
        factura.push({id: productoId, nombre, cantidad, precio});
      }

      actualizarTabla();
    });

    tablaFacturaBody.addEventListener('click', e => {
      if(e.target.classList.contains('btn-eliminar')) {
        const index = parseInt(e.target.getAttribute('data-index'));
        factura.splice(index, 1);
        actualizarTabla();
      }
    });

    btnConfirmar.addEventListener('click', () => {
      if (factura.length === 0) return;

      if(!confirm("¿Confirmar venta? Esta acción reducirá el stock.")) {
        return;
      }

      const items = factura.map(item => ({
        id: parseInt(item.id),
        nombre: item.nombre,
        cantidad: item.cantidad
      }));

      fetch("/ventas/confirmar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({items})
      })
      .then(response => {
        if(!response.ok) {
          return response.json().then(data => { throw new Error(data.detail || "Error desconocido"); });
        }
        return response.json();
      })
      .then(data => {
        alert(data.msg);
        factura = [];
        actualizarTabla();
        location.reload();
      })
      .catch(err => alert("Error: " + err.message));
    });

  });