// ============================================================
// VALIDACIÓN FORMULARIO DE VEHÍCULOS
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[novalidate]");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        let valido = true;

        // Limpiar estados previos
        form.querySelectorAll(".is-invalid").forEach((el) =>
            el.classList.remove("is-invalid")
        );

        // Se corrigieron los nombres de los campos de ID según la convención de la ruta.py
        const placa = form.placa.value.trim();
        const marca = form.marca.value.trim();
        const modelo = form.modelo.value.trim();
        const anio = parseInt(form.anio.value.trim());
        const tipo = form.tipo_id.value.trim(); 
        const capacidad = parseFloat(form.capacidad.value.trim());
        const estado = form.estado_id.value.trim();

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
        if (!marca) {
            marcarInvalido(form.marca, "La marca no puede estar vacía.");
            valido = false;
        }

        // Modelo
        if (!modelo) {
            marcarInvalido(form.modelo, "El modelo es obligatorio.");
            valido = false;
        }

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
        if (!tipo) {
            marcarInvalido(form.tipo_id, "Seleccione un tipo de vehículo.");
            valido = false;
        }

        // Capacidad
        if (isNaN(capacidad) || capacidad <= 0) {
            marcarInvalido(
                form.capacidad,
                "Ingrese una capacidad de carga válida (mayor a 0)."
            );
            valido = false;
        }

        // Estado
        if (!estado) {
            marcarInvalido(form.estado_id, "Seleccione el estado del vehículo.");
            valido = false;
        }

        if (!valido) {
            e.preventDefault();
            mostrarAlerta(
                "Por favor, corrija los campos marcados en rojo ⚠️",
                "danger"
            );
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

// ============================================================
// VALIDACIÓN Y FILTRO FORMULARIO DE UBICACIONES (REGISTRO)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    const formUbicacion = document.getElementById("form-ubicacion");
    const selectDepto = document.getElementById("ubicacion-departamento");
    const selectMunicipio = document.getElementById("ubicacion-municipio");

    // --- Filtro dinámico de municipios según el departamento ---
    if (selectDepto && selectMunicipio) {
        // Capturamos todos los optgroups (municipios agrupados por departamento)
        const grupos = Array.from(selectMunicipio.querySelectorAll("optgroup"));

        function filtrarMunicipios() {
            const depto = selectDepto.value;
            
            // Ocultamos todos los grupos inicialmente
            grupos.forEach((g) => (g.style.display = "none"));

            if (!depto) {
                // Si no hay departamento seleccionado, deshabilita y resetea
                selectMunicipio.disabled = true;
                selectMunicipio.value = "";
                return;
            }

            // Habilitar el selector de municipios y limpiar su valor
            selectMunicipio.disabled = false;
            selectMunicipio.value = ""; // Limpiamos la selección anterior

            // Mostrar solo los grupos que coinciden con el departamento seleccionado
            grupos.forEach((g) => {
                g.style.display = g.dataset.parent === depto ? "block" : "none";
            });
        }

        // Estado inicial al cargar:
        // 1. Ocultamos todos los municipios.
        // 2. Deshabilitamos el selector de municipios.
        grupos.forEach((g) => (g.style.display = "none"));
        selectMunicipio.disabled = true;

        // 💡 CORRECCIÓN CLAVE: Ejecutar el filtro si hay un departamento preseleccionado
        if (selectDepto.value) {
            filtrarMunicipios();
        }

        // 3. Establecer el listener para cuando el usuario cambie el departamento
        selectDepto.addEventListener("change", filtrarMunicipios);
    }

    // --- Validación del formulario ---
    if (formUbicacion) {
        formUbicacion.addEventListener("submit", (e) => {
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
                formUbicacion.submit();
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
        form
            .querySelectorAll(".is-invalid")
            .forEach((el) => el.classList.remove("is-invalid"));
        form
            .querySelectorAll(".invalid-feedback")
            .forEach((el) => el.remove());
    }

    function mostrarAlerta(mensaje, tipo, form) {
        const alerta = document.createElement("div");
        alerta.className = `alert alert-${tipo} mt-3`;

        const container = form.closest(".card") || form; 
        
        container.querySelectorAll(".alert").forEach(a => a.remove());

        alerta.textContent = mensaje;

        container.prepend(alerta);
        setTimeout(() => alerta.remove(), 4000);
    }
});

// ============================================================
// VALIDACIÓN Y FILTRO FORMULARIO DE UBICACIONES (DETALLES)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {

    const selectDepto = document.getElementById("detalle-departamento");
    const selectMunicipio = document.getElementById("detalle-municipio");

    if (selectDepto && selectMunicipio) {

        const grupos = Array.from(selectMunicipio.querySelectorAll("optgroup"));

        function filtrarMunicipios() {
            const depto = selectDepto.value;

            grupos.forEach(g => g.style.display = "none");

            if (!depto) {
                selectMunicipio.disabled = true;
                selectMunicipio.value = "";
                return;
            }

            selectMunicipio.disabled = false;
            selectMunicipio.value = "";

            grupos.forEach(g => {
                g.style.display = g.dataset.parent === depto ? "block" : "none";
            });
        }

        // Estado inicial: ocultar todos
        grupos.forEach(g => g.style.display = "none");
        selectMunicipio.disabled = true;

        // Si ya viene preseleccionado el departamento → activar el filtro
        if (selectDepto.value) {
            filtrarMunicipios();
            selectMunicipio.value = "{{ m.Id_Municipio }}";
        }

        selectDepto.addEventListener("change", filtrarMunicipios);
    }
});


// ============================================================
// VALIDACIÓN Y FORMATEO DE CONDUCTORES (MODAL)
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formConductor");
    const modalElement = document.getElementById("modalRegistroConductor");
    if (!form || !modalElement) return;

    // Campos
    const nombre = document.getElementById("nombre");
    const dui = document.getElementById("dui");
    const licencia = document.getElementById("licencia");
    const telefono = document.getElementById("telefono");
    const fechaVencimiento = document.getElementById("fechaVencimiento");

    // Formateos en tiempo real 
    if (nombre) {
        nombre.addEventListener("input", () => {
            nombre.value = nombre.value.replace(
                /[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g,
                ""
            );
        });
    }

    if (dui) {
        dui.addEventListener("input", () => {
            let valor = dui.value.replace(/\D/g, "").slice(0, 9);
            if (valor.length > 8)
                valor = valor.slice(0, 8) + "-" + valor.slice(8);
            dui.value = valor;
        });
    }

    if (licencia) {
        licencia.addEventListener("input", () => {
            let valor = licencia.value.replace(/\D/g, "").slice(0, 14);
            if (valor.length > 4) valor = valor.slice(0, 4) + "-" + valor.slice(4);
            if (valor.length > 11)
                valor = valor.slice(0, 11) + "-" + valor.slice(11);
            if (valor.length > 15)
                valor = valor.slice(0, 15) + "-" + valor.slice(15);
            licencia.value = valor;
        });
    }

    if (telefono) {
        telefono.addEventListener("input", () => {
            let valor = telefono.value.replace(/\D/g, "").slice(0, 8);
            if (valor.length > 4)
                valor = valor.slice(0, 4) + "-" + valor.slice(4);
            telefono.value = valor;
        });
    }


    // Validación del formulario
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        event.stopPropagation();

        let valido = true;

        // Validación de formato DUI
        if (dui && !/^\d{8}-\d$/.test(dui.value)) {
            dui.classList.add("is-invalid");
            valido = false;
        } else if (dui) {
            dui.classList.remove("is-invalid");
        }

        // Validación de formato Licencia
        if (licencia && !/^\d{4}-\d{6}-\d{3}-\d$/.test(licencia.value)) {
            licencia.classList.add("is-invalid");
            valido = false;
        } else if (licencia) {
            licencia.classList.remove("is-invalid");
        }

        // Validación de formato Teléfono
        if (telefono && !/^\d{4}-\d{4}$/.test(telefono.value)) {
            telefono.classList.add("is-invalid");
            valido = false;
        } else if (telefono) {
            telefono.classList.remove("is-invalid");
        }

        // Validación de fecha de vencimiento
        if (fechaVencimiento) {
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            const fechaIngresada = new Date(fechaVencimiento.value);

            if (fechaIngresada < hoy || !fechaVencimiento.value) {
                fechaVencimiento.classList.add("is-invalid");
                valido = false;
            } else {
                fechaVencimiento.classList.remove("is-invalid");
            }
        }
        
        form.classList.add("was-validated");

        if (form.checkValidity() && valido) {
             form.submit();
        }
    });
    
    // Función para limpiar el modal al cerrarse (asumiendo que Bootstrap está cargado)
    if (typeof bootstrap !== 'undefined') {
        const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        modalElement.addEventListener("hidden.bs.modal", () => {
            form.reset();
            form.classList.remove("was-validated");
            form
                .querySelectorAll(".is-invalid")
                .forEach((el) => el.classList.remove("is-invalid"));
        });
    }
    
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