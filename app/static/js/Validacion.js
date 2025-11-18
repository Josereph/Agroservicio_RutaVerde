<<<<<<< HEAD
// ============================================================
// VALIDACIÓN FORMULARIO DE VEHÍCULOS
// ============================================================
=======
>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[novalidate]");
  if (!form) return;

  form.addEventListener("submit", (e) => {
<<<<<<< HEAD
    let valido = true;

    // Limpiar estados previos
    form.querySelectorAll(".is-invalid").forEach((el) =>
      el.classList.remove("is-invalid")
    );
=======
    e.preventDefault();
    let valido = true;

    form.querySelectorAll(".is-invalid").forEach((el) => el.classList.remove("is-invalid"));
>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)

    const placa = form.placa.value.trim();
    const marca = form.marca.value.trim();
    const modelo = form.modelo.value.trim();
    const anio = parseInt(form.anio.value.trim());
    const tipo = form.tipo.value.trim();
    const capacidad = parseFloat(form.capacidad.value.trim());
    const estado = form.estado.value.trim();

<<<<<<< HEAD
    // Validación de placa
    const placaRegex = /^[A-Z]{1,2}-?\d{3,6}$/;
    if (!placa || !placaRegex.test(placa)) {
      marcarInvalido(
        form.placa,
        "Formato de placa incorrecto (Ej: P-123456 o AB123456)."
      );
      valido = false;
    }

    // Marca
=======
    const placaRegex = /^[A-Z]{1,2}-?\d{3,6}$/;
    if (!placa || !placaRegex.test(placa)) {
      marcarInvalido(form.placa, "Formato de placa incorrecto (Ej: P-123456 o AB123456).");
      valido = false;
    }

>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
    if (!marca) {
      marcarInvalido(form.marca, "La marca no puede estar vacía.");
      valido = false;
    }

<<<<<<< HEAD
    // Modelo
=======
>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
    if (!modelo) {
      marcarInvalido(form.modelo, "El modelo es obligatorio.");
      valido = false;
    }

<<<<<<< HEAD
    // Año
    const yearActual = new Date().getFullYear();
    if (isNaN(anio) || anio < 1980 || anio > yearActual + 1) {
      marcarInvalido(
        form.anio,
        `El año debe estar entre 1980 y ${yearActual + 1}.`
      );
      valido = false;
    }

    // Tipo
=======
    const yearActual = new Date().getFullYear();
    if (isNaN(anio) || anio < 1980 || anio > yearActual + 1) {
      marcarInvalido(form.anio, `El año debe estar entre 1980 y ${yearActual + 1}.`);
      valido = false;
    }


>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
    if (!tipo) {
      marcarInvalido(form.tipo, "Seleccione un tipo de vehículo.");
      valido = false;
    }

<<<<<<< HEAD
    // Capacidad
    if (isNaN(capacidad) || capacidad <= 0) {
      marcarInvalido(
        form.capacidad,
        "Ingrese una capacidad de carga válida (mayor a 0)."
      );
      valido = false;
    }

    // Estado
=======
    if (isNaN(capacidad) || capacidad <= 0) {
      marcarInvalido(form.capacidad, "Ingrese una capacidad de carga válida (mayor a 0).");
      valido = false;
    }


>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
    if (!estado) {
      marcarInvalido(form.estado, "Seleccione el estado del vehículo.");
      valido = false;
    }

<<<<<<< HEAD
    if (!valido) {
      e.preventDefault();
      mostrarAlerta(
        "Por favor, corrija los campos marcados en rojo ⚠️",
        "danger"
      );
    }
  });

=======

    if (valido) {
      mostrarAlerta("Vehículo guardado correctamente ✅", "success");
      form.reset();
    } else {
      mostrarAlerta("Por favor, corrija los campos marcados en rojo ⚠️", "danger");
    }
  });


>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
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

<<<<<<< HEAD
// ============================================================
// VALIDACIÓN Y FILTRO FORMULARIO DE UBICACIONES (REGISTRO)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
=======

document.addEventListener("DOMContentLoaded", () => {
  // ======== VALIDACIÓN FORMULARIO DE UBICACIONES ========
>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
  const formUbicacion = document.getElementById("form-ubicacion");
  const selectDepto = document.getElementById("ubicacion-departamento");
  const selectMunicipio = document.getElementById("ubicacion-municipio");

  // --- Filtro dinámico de municipios según el departamento ---
  if (selectDepto && selectMunicipio) {
    const grupos = Array.from(selectMunicipio.querySelectorAll("optgroup"));
<<<<<<< HEAD

    function filtrarMunicipios() {
      const depto = selectDepto.value;
      selectMunicipio.value = "";

      if (!depto) {
        selectMunicipio.disabled = true;
        grupos.forEach((g) => (g.style.display = "none"));
        return;
      }

      selectMunicipio.disabled = false;

      grupos.forEach((g) => {
        g.style.display = g.dataset.parent === depto ? "block" : "none";
      });
    }

    // Estado inicial
    grupos.forEach((g) => (g.style.display = "none"));
    selectMunicipio.disabled = true;

    selectDepto.addEventListener("change", filtrarMunicipios);
=======
    grupos.forEach(g => g.style.display = "none");

    selectDepto.addEventListener("change", () => {
      const depto = selectDepto.value;
      selectMunicipio.value = "";
      grupos.forEach(g => {
        g.style.display = g.dataset.parent === depto ? "block" : "none";
      });
    });
>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
  }

  // --- Validación del formulario ---
  if (formUbicacion) {
    formUbicacion.addEventListener("submit", (e) => {
<<<<<<< HEAD
  e.preventDefault();
  limpiarMensajes(formUbicacion);

  const depto = selectDepto.value.trim();
  const municipio = selectMunicipio.value.trim();
  const direccion = document.getElementById("ubicacion-direccion").value.trim();
  let valido = true;

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

  if (valido) {
    // 👉 Aquí ya NO reseteamos: dejamos que vaya al backend
    formUbicacion.submit();
  } else {
    mostrarAlerta("⚠️ Corrige los campos marcados antes de continuar", "danger", formUbicacion);
  }
});

  }
=======
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

>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)

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
<<<<<<< HEAD
    form
      .querySelectorAll(".is-invalid")
      .forEach((el) => el.classList.remove("is-invalid"));
    form
      .querySelectorAll(".invalid-feedback")
      .forEach((el) => el.remove());
=======
    form.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
    form.querySelectorAll(".invalid-feedback").forEach(el => el.remove());
>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
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

<<<<<<< HEAD
// ============================================================
// DETALLE DE UBICACIÓN (EDICIÓN)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-detalle-ubicacion");
  if (!form) return;

  const departamentoSelect = document.getElementById("detalle-departamento");
  const municipioSelect = document.getElementById("detalle-municipio");

  // Filtro dinámico de municipios según departamento
  departamentoSelect.addEventListener("change", () => {
    const departamento = departamentoSelect.value;
    const grupos = municipioSelect.querySelectorAll("optgroup");
    municipioSelect.value = "";

    grupos.forEach((g) => {
      g.style.display =
        g.getAttribute("data-parent") === departamento
          ? "block"
          : "none";
    });
  });

  // Aplicar filtro al cargar (para que coincida con el depto seleccionado)
  departamentoSelect.dispatchEvent(new Event("change"));

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const nombre = document
      .getElementById("detalle-nombre")
      .value.trim();
    const codigo = document
      .getElementById("detalle-codigo")
      .value.trim();
    const departamento = departamentoSelect.value;
    const municipio = municipioSelect.value;
    const direccion = document
      .getElementById("detalle-direccion")
      .value.trim();
    const estado = document.getElementById("detalle-estado").value;

    if (!nombre) return alert("El nombre de la ubicación o ruta es obligatorio.");
    if (nombre.length < 3)
      return alert("El nombre debe tener al menos 3 caracteres.");
    if (!codigo) return alert("El código es obligatorio.");
    if (!departamento) return alert("Debes seleccionar un departamento.");
    if (municipio === "" && direccion === "") {
      const confirmar = confirm(
        "No seleccionaste municipio ni dirección. ¿Deseas guardar esta ubicación como jerarquía superior?"
      );
      if (!confirmar) return;
    }
    if (estado !== "activo" && estado !== "inactivo")
      return alert("Selecciona un estado válido.");

    alert("Validación exitosa. Guardando cambios...");
    form.submit();
  });
});

// ============================================================
// FORMULARIO DE SERVICIOS (REGISTRO)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#registro form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
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

// ============================================================
// GESTIÓN DE EVIDENCIA Y SEGUIMIENTO
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  // === VALIDAR REGISTRO DE EVIDENCIA ===
  const formEvidencia = document.querySelector("#registrar form");
  if (formEvidencia) {
    formEvidencia.addEventListener("submit", (e) => {
      e.preventDefault();

      const servicio = formEvidencia.id_servicio.value;
      const tipoEvidencia = formEvidencia.tipo_evidencia.value;
      const archivo = formEvidencia.archivo.files[0];
      const legible = formEvidencia.es_legible.value;
      const fechaCaptura = formEvidencia.fecha_captura.value;

      let valido = true;

      if (!servicio) valido = false;
      if (!tipoEvidencia) valido = false;

      if (!archivo) valido = false;
      else {
        const tiposPermitidos = [
          "image/jpeg",
          "image/png",
          "application/pdf",
        ];
        if (!tiposPermitidos.includes(archivo.type)) valido = false;
        if (archivo.size > 5 * 1024 * 1024) valido = false;
      }

      if (!fechaCaptura) valido = false;
      if (legible !== "1" && legible !== "0") valido = false;

      if (valido) formEvidencia.submit();
    });
  }

  // === VALIDAR REGISTRO DE SEGUIMIENTO ===
  const formSeguimiento = document.querySelector("#seguimiento form");
  if (formSeguimiento) {
    formSeguimiento.addEventListener("submit", (e) => {
      e.preventDefault();

      const servicio = formSeguimiento.id_servicio.value;
      const estadoActual = formSeguimiento.estado_actual.value;
      const controlCalidad = formSeguimiento.control_calidad.value;
      const incidente = formSeguimiento.incidente.value.trim();
      const notificado =
        formSeguimiento.notificacion_enviada?.checked;
      const receptor =
        formSeguimiento.nombre_receptor.value.trim();

      let valido = true;

      if (!servicio) valido = false;
      if (!estadoActual) valido = false;
      if (!controlCalidad) valido = false;

      if (estadoActual === "entregado" && receptor === "")
        valido = false;

      if (incidente && incidente.length < 5) valido = false;

      if (valido) formSeguimiento.submit();
    });
  }
});

// ============================================================
// VALIDACIÓN Y FORMATEO DE CONDUCTORES (MODAL)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formConductor");
  const modalElement = document.getElementById("modalRegistroConductor");
  if (!form || !modalElement) return;

  const modal = bootstrap.Modal.getOrCreateInstance(modalElement);

  // Campos
  const nombre = document.getElementById("nombre");
  const dui = document.getElementById("dui");
  const licencia = document.getElementById("licencia");
  const telefono = document.getElementById("telefono");
  const fechaVencimiento = document.getElementById("fechaVencimiento");

  // Formateos en tiempo real
  nombre.addEventListener("input", () => {
    nombre.value = nombre.value.replace(
      /[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g,
      ""
    );
  });

  dui.addEventListener("input", () => {
    let valor = dui.value.replace(/\D/g, "").slice(0, 9);
    if (valor.length > 8)
      valor = valor.slice(0, 8) + "-" + valor.slice(8);
    dui.value = valor;
  });

  licencia.addEventListener("input", () => {
    let valor = licencia.value.replace(/\D/g, "").slice(0, 14);
    if (valor.length > 4) valor = valor.slice(0, 4) + "-" + valor.slice(4);
    if (valor.length > 11)
      valor = valor.slice(0, 11) + "-" + valor.slice(11);
    if (valor.length > 15)
      valor = valor.slice(0, 15) + "-" + valor.slice(15);
    licencia.value = valor;
  });

  telefono.addEventListener("input", () => {
    let valor = telefono.value.replace(/\D/g, "").slice(0, 8);
    if (valor.length > 4)
      valor = valor.slice(0, 4) + "-" + valor.slice(4);
    telefono.value = valor;
  });

  // Validación del formulario
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    event.stopPropagation();

    let valido = true;

    if (!/^\d{8}-\d$/.test(dui.value)) {
      dui.classList.add("is-invalid");
      valido = false;
    } else {
      dui.classList.remove("is-invalid");
    }

    if (!/^\d{4}-\d{6}-\d{3}-\d$/.test(licencia.value)) {
      licencia.classList.add("is-invalid");
      valido = false;
    } else {
      licencia.classList.remove("is-invalid");
    }

    if (!/^\d{4}-\d{4}$/.test(telefono.value)) {
      telefono.classList.add("is-invalid");
      valido = false;
    } else {
      telefono.classList.remove("is-invalid");
    }

    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    const fechaIngresada = new Date(fechaVencimiento.value);
    if (fechaIngresada < hoy || !fechaVencimiento.value) {
      fechaVencimiento.classList.add("is-invalid");
      valido = false;
    } else {
      fechaVencimiento.classList.remove("is-invalid");
    }

    form.classList.add("was-validated");

    if (form.checkValidity() && valido) {
      const datosConductor = {
        nombre: nombre.value,
        dui: dui.value,
        licencia: licencia.value,
        telefono: telefono.value,
        estado: document.getElementById("estado").value,
      };

      agregarConductorATabla(datosConductor);
      modal.hide();
      form.reset();
      form.classList.remove("was-validated");
      form
        .querySelectorAll(".is-invalid")
        .forEach((el) => el.classList.remove("is-invalid"));
    }
  });

  modalElement.addEventListener("hidden.bs.modal", () => {
    form.reset();
    form.classList.remove("was-validated");
    form
      .querySelectorAll(".is-invalid")
      .forEach((el) => el.classList.remove("is-invalid"));
  });
});

// --- Función para agregar dinámicamente un conductor a la tabla ---
function agregarConductorATabla(conductor) {
  const tablaBody = document.getElementById("tablaConductoresBody");
  const nuevaFila = tablaBody.insertRow(0);

  let badgeClass = "";
  let textClass = "";
  switch (conductor.estado) {
    case "Activo":
      badgeClass = "bg-success-subtle";
      textClass = "text-success-emphasis";
      break;
    case "Inactivo":
      badgeClass = "bg-danger-subtle";
      textClass = "text-danger-emphasis";
      break;
    case "Suspendido":
      badgeClass = "bg-warning-subtle";
      textClass = "text-warning-emphasis";
      break;
    default:
      badgeClass = "bg-secondary-subtle";
      textClass = "text-secondary-emphasis";
  }

  nuevaFila.innerHTML = `
    <td>${conductor.nombre}</td>
    <td>${conductor.dui}</td>
    <td>${conductor.licencia}</td>
    <td>${conductor.telefono}</td>
    <td>
      <span class="badge ${badgeClass} ${textClass} rounded-pill">${conductor.estado}</span>
    </td>
    <td class="text-end">
      <button class="btn btn-sm btn-outline-primary me-1" title="Editar">
        <i class="bi bi-pencil-fill"></i>
      </button>
      <button class="btn btn-sm btn-outline-danger" title="Desactivar">
        <i class="bi bi-trash-fill"></i>
      </button>
    </td>
  `;
}
=======

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



>>>>>>> bb3ae60 (creacion de validacion de todas las vistas)
