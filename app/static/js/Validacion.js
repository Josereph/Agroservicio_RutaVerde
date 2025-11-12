document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[novalidate]");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let valido = true;

    form.querySelectorAll(".is-invalid").forEach((el) => el.classList.remove("is-invalid"));

    const placa = form.placa.value.trim();
    const marca = form.marca.value.trim();
    const modelo = form.modelo.value.trim();
    const anio = parseInt(form.anio.value.trim());
    const tipo = form.tipo.value.trim();
    const capacidad = parseFloat(form.capacidad.value.trim());
    const estado = form.estado.value.trim();

    const placaRegex = /^[A-Z]{1,2}-?\d{3,6}$/;
    if (!placa || !placaRegex.test(placa)) {
      marcarInvalido(form.placa, "Formato de placa incorrecto (Ej: P-123456 o AB123456).");
      valido = false;
    }

    if (!marca) {
      marcarInvalido(form.marca, "La marca no puede estar vacía.");
      valido = false;
    }

    if (!modelo) {
      marcarInvalido(form.modelo, "El modelo es obligatorio.");
      valido = false;
    }

    const yearActual = new Date().getFullYear();
    if (isNaN(anio) || anio < 1980 || anio > yearActual + 1) {
      marcarInvalido(form.anio, `El año debe estar entre 1980 y ${yearActual + 1}.`);
      valido = false;
    }


    if (!tipo) {
      marcarInvalido(form.tipo, "Seleccione un tipo de vehículo.");
      valido = false;
    }

    if (isNaN(capacidad) || capacidad <= 0) {
      marcarInvalido(form.capacidad, "Ingrese una capacidad de carga válida (mayor a 0).");
      valido = false;
    }


    if (!estado) {
      marcarInvalido(form.estado, "Seleccione el estado del vehículo.");
      valido = false;
    }


    if (valido) {
      mostrarAlerta("Vehículo guardado correctamente ✅", "success");
      form.reset();
    } else {
      mostrarAlerta("Por favor, corrija los campos marcados en rojo ⚠️", "danger");
    }
  });


  function marcarInvalido(campo, mensaje) {
    campo.classList.add("is-invalid");
    let feedback = campo.nextElementSibling;
    if (!feedback || !feedback.classList.contains("invalid-feedback")) {
      feedback = document.createElement("div");
      feedback.classList.add("invalid-feedback");
      campo.insertAdjacentElement("afterend", feedback);
    }
    feedback.textContent = mensaje;
  }

  function mostrarAlerta(mensaje, tipo = "success") {
    const alert = document.createElement("div");
    alert.className = `alert alert-${tipo} mt-3`;
    alert.textContent = mensaje;

    const container = form.closest(".card") || document.body;
    container.prepend(alert);

    setTimeout(() => alert.remove(), 4000);
  }
});


document.addEventListener("DOMContentLoaded", () => {
  // ======== VALIDACIÓN FORMULARIO DE UBICACIONES ========
  const formUbicacion = document.getElementById("form-ubicacion");
  const selectDepto = document.getElementById("ubicacion-departamento");
  const selectMunicipio = document.getElementById("ubicacion-municipio");

  // --- Filtro dinámico de municipios según el departamento ---
  if (selectDepto && selectMunicipio) {
    const grupos = Array.from(selectMunicipio.querySelectorAll("optgroup"));
    grupos.forEach(g => g.style.display = "none");

    selectDepto.addEventListener("change", () => {
      const depto = selectDepto.value;
      selectMunicipio.value = "";
      grupos.forEach(g => {
        g.style.display = g.dataset.parent === depto ? "block" : "none";
      });
    });
  }

  // --- Validación del formulario ---
  if (formUbicacion) {
    formUbicacion.addEventListener("submit", (e) => {
      e.preventDefault();
      limpiarMensajes(formUbicacion);

      const depto = selectDepto.value.trim();
      const municipio = selectMunicipio.value.trim();
      const direccion = document.getElementById("ubicacion-direccion").value.trim();
      const estado = document.getElementById("ubicacion-estado").value.trim();
      let valido = true;

      // Validaciones básicas
      if (!depto) {
        marcarInvalido(selectDepto, "Debe seleccionar un departamento.");
        valido = false;
      }

      if (!municipio) {
        marcarInvalido(selectMunicipio, "Seleccione un municipio válido.");
        valido = false;
      }

      if (direccion.length < 5) {
        marcarInvalido(document.getElementById("ubicacion-direccion"), "Ingrese una dirección más detallada.");
        valido = false;
      }

      if (!estado) {
        marcarInvalido(document.getElementById("ubicacion-estado"), "Debe indicar el estado.");
        valido = false;
      }

      if (valido) {
        mostrarAlerta("✅ Ubicación registrada correctamente", "success", formUbicacion);
        formUbicacion.reset();
      } else {
        mostrarAlerta("⚠️ Corrige los campos marcados antes de continuar", "danger", formUbicacion);
      }
    });
  }


  function marcarInvalido(campo, mensaje) {
    campo.classList.add("is-invalid");
    let feedback = campo.nextElementSibling;
    if (!feedback || !feedback.classList.contains("invalid-feedback")) {
      feedback = document.createElement("div");
      feedback.classList.add("invalid-feedback");
      campo.insertAdjacentElement("afterend", feedback);
    }
    feedback.textContent = mensaje;
  }

  function limpiarMensajes(form) {
    form.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
    form.querySelectorAll(".invalid-feedback").forEach(el => el.remove());
  }

  function mostrarAlerta(mensaje, tipo, form) {
    const alerta = document.createElement("div");
    alerta.className = `alert alert-${tipo} mt-3`;
    alerta.textContent = mensaje;

    const card = form.closest(".card");
    card.prepend(alerta);
    setTimeout(() => alerta.remove(), 4000);
  }
});


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-detalle-ubicacion");
    if (!form) return;

    const departamentoSelect = document.getElementById("detalle-departamento");
    const municipioSelect = document.getElementById("detalle-municipio");

    departamentoSelect.addEventListener("change", () => {
        const departamento = departamentoSelect.value;
        const grupos = municipioSelect.querySelectorAll("optgroup");
        municipioSelect.value = "";
        grupos.forEach(g => {
            g.style.display = g.getAttribute("data-parent") === departamento ? "block" : "none";
        });
    });
    departamentoSelect.dispatchEvent(new Event("change"));

    form.addEventListener("submit", e => {
        e.preventDefault();
        const nombre = document.getElementById("detalle-nombre").value.trim();
        const codigo = document.getElementById("detalle-codigo").value.trim();
        const departamento = departamentoSelect.value;
        const municipio = municipioSelect.value;
        const direccion = document.getElementById("detalle-direccion").value.trim();
        const estado = document.getElementById("detalle-estado").value;

        if (!nombre) return alert("El nombre de la ubicación o ruta es obligatorio.");
        if (nombre.length < 3) return alert("El nombre debe tener al menos 3 caracteres.");
        if (!codigo) return alert("El código es obligatorio.");
        if (!/^[A-Z]{2,4}$/.test(codigo)) return alert("El código debe tener entre 2 y 4 letras mayúsculas.");
        if (!departamento) return alert("Debes seleccionar un departamento.");
        if (municipio === "" && direccion === "") {
            const confirmar = confirm("No seleccionaste municipio ni dirección. ¿Deseas guardar esta ubicación como jerarquía superior?");
            if (!confirmar) return;
        }
        if (estado !== "activo" && estado !== "inactivo") return alert("Selecciona un estado válido.");

        alert("Validación exitosa. Guardando cambios...");
        form.submit();
    });
});document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-detalle-ubicacion");
    if (!form) return;

    const departamentoSelect = document.getElementById("detalle-departamento");
    const municipioSelect = document.getElementById("detalle-municipio");

    departamentoSelect.addEventListener("change", () => {
        const departamento = departamentoSelect.value;
        const grupos = municipioSelect.querySelectorAll("optgroup");
        municipioSelect.value = "";
        grupos.forEach(g => {
            g.style.display = g.getAttribute("data-parent") === departamento ? "block" : "none";
        });
    });
    departamentoSelect.dispatchEvent(new Event("change"));

    form.addEventListener("submit", e => {
        e.preventDefault();
        const nombre = document.getElementById("detalle-nombre").value.trim();
        const codigo = document.getElementById("detalle-codigo").value.trim();
        const departamento = departamentoSelect.value;
        const municipio = municipioSelect.value;
        const direccion = document.getElementById("detalle-direccion").value.trim();
        const estado = document.getElementById("detalle-estado").value;

        let valido = true;

        if (!nombre || nombre.length < 3) valido = false;
        if (!codigo || !/^[A-Z]{2,4}$/.test(codigo)) valido = false;
        if (!departamento) valido = false;
        if (municipio === "" && direccion === "") valido = false;
        if (estado !== "activo" && estado !== "inactivo") valido = false;

        if (valido) form.submit();
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#registro form");
    if (!form) return;

    form.addEventListener("submit", e => {
        e.preventDefault();
        const nombre = form.cliente_nombre.value.trim();
        const email = form.cliente_email.value.trim();
        const tipoServicio = form.tipo_servicio.value;
        const nombreProducto = form.nombre_producto.value.trim();
        const tipoProducto = form.tipo_producto.value.trim();
        const cantidad = parseFloat(form.cantidad.value);
        const peso = parseFloat(form.peso_carga.value);
        const origen = form.ubicacion_origen.value.trim();
        const destino = form.destino.value.trim();
        const fechaInicio = new Date(form.fecha_inicio.value);
        const fechaEntrega = new Date(form.fecha_entrega.value);
        const precio = parseFloat(form.precio_total.value);
        const metodoPago = form.metodo_pago.value;

        let valido = true;

        if (!nombre || nombre.length < 3) valido = false;
        if (!email || !/\S+@\S+\.\S+/.test(email)) valido = false;
        if (!tipoServicio) valido = false;
        if (!nombreProducto || !tipoProducto) valido = false;
        if (isNaN(cantidad) || cantidad <= 0) valido = false;
        if (isNaN(peso) || peso <= 0) valido = false;
        if (!origen || !destino) valido = false;
        if (!form.fecha_inicio.value || !form.fecha_entrega.value) valido = false;
        if (fechaEntrega <= fechaInicio) valido = false;
        if (isNaN(precio) || precio <= 0) valido = false;
        if (!metodoPago) valido = false;

        if (valido) form.submit();
    });
});




document.addEventListener("DOMContentLoaded", () => {
    // === VALIDAR REGISTRO DE EVIDENCIA ===
    const formEvidencia = document.querySelector('#registrar form');
    if (formEvidencia) {
        formEvidencia.addEventListener("submit", e => {
            e.preventDefault();

            const servicio = formEvidencia.id_servicio.value;
            const tipoEvidencia = formEvidencia.tipo_evidencia.value;
            const archivo = formEvidencia.archivo.files[0];
            const legible = formEvidencia.es_legible.value;
            const fechaCaptura = formEvidencia.fecha_captura.value;

            let valido = true;

            if (!servicio) valido = false;
            if (!tipoEvidencia) valido = false;

            // Validar archivo
            if (!archivo) valido = false;
            else {
                const tiposPermitidos = ["image/jpeg", "image/png", "application/pdf"];
                if (!tiposPermitidos.includes(archivo.type)) valido = false;
                if (archivo.size > 5 * 1024 * 1024) valido = false; // máximo 5MB
            }

            if (!fechaCaptura) valido = false;
            if (legible !== "1" && legible !== "0") valido = false;

            if (valido) formEvidencia.submit();
        });
    }

    // === VALIDAR REGISTRO DE SEGUIMIENTO ===
    const formSeguimiento = document.querySelector('#seguimiento form');
    if (formSeguimiento) {
        formSeguimiento.addEventListener("submit", e => {
            e.preventDefault();

            const servicio = formSeguimiento.id_servicio.value;
            const estadoActual = formSeguimiento.estado_actual.value;
            const controlCalidad = formSeguimiento.control_calidad.value;
            const incidente = formSeguimiento.incidente.value.trim();
            const notificado = formSeguimiento.notificacion_enviada?.checked;
            const receptor = formSeguimiento.nombre_receptor.value.trim();

            let valido = true;

            if (!servicio) valido = false;
            if (!estadoActual) valido = false;
            if (!controlCalidad) valido = false;

            if (estadoActual === "entregado" && receptor === "") valido = false;

            if (incidente && incidente.length < 5) valido = false;

            if (valido) formSeguimiento.submit();
        });
    }
});



