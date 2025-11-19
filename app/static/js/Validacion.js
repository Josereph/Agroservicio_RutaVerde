// ============================================================
// VALIDACIÓN FORMULARIO DE VEHÍCULOS
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form[novalidate]");
    if (form) {
        form.addEventListener("submit", (e) => {
            let valido = true;

            // limpiar invalid
            form.querySelectorAll(".is-invalid").forEach((el) =>
                el.classList.remove("is-invalid")
            );

            const placa = form.placa.value.trim();
            const marca = form.marca.value.trim();
            const modelo = form.modelo.value.trim();
            const anio = parseInt(form.anio.value.trim());
            const tipo = form.tipo_id.value.trim();
            const capacidad = parseFloat(form.capacidad.value.trim());
            const estado = form.estado_id.value.trim();

            // placa
            const placaRegex = /^[A-Z]{1,2}-?\d{3,6}$/;
            if (!placa || !placaRegex.test(placa)) {
                marcarInvalido(
                    form.placa,
                    "Formato de placa incorrecto (Ej: P-123456 o AB123456)."
                );
                valido = false;
            }

            // marca
            if (!marca) {
                marcarInvalido(form.marca, "La marca no puede estar vacía.");
                valido = false;
            }

            // modelo
            if (!modelo) {
                marcarInvalido(form.modelo, "El modelo es obligatorio.");
                valido = false;
            }

            // año
            const yearActual = new Date().getFullYear();
            if (isNaN(anio) || anio < 1980 || anio > yearActual + 1) {
                marcarInvalido(
                    form.anio,
                    `El año debe estar entre 1980 y ${yearActual + 1}.`
                );
                valido = false;
            }

            // tipo
            if (!tipo) {
                marcarInvalido(form.tipo_id, "Seleccione un tipo de vehículo.");
                valido = false;
            }

            // capacidad
            if (isNaN(capacidad) || capacidad <= 0) {
                marcarInvalido(
                    form.capacidad,
                    "Ingrese una capacidad válida (mayor a 0)."
                );
                valido = false;
            }

            if (!estado) {
                marcarInvalido(form.estado_id, "Seleccione un estado.");
                valido = false;
            }

            if (!valido) {
                e.preventDefault();
                mostrarAlerta(
                    "Por favor, corrija los campos marcados en rojo ⚠",
                    "danger",
                    form
                );
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

    function mostrarAlerta(mensaje, tipo = "success", form) {
        const alert = document.createElement("div");
        alert.className = `alert alert-${tipo} mt-3`;
        alert.textContent = mensaje;

        const container = form.closest(".card") || document.body;
        container.prepend(alert);

        setTimeout(() => alert.remove(), 4000);
    }
});

// ============================================================
// FORMULARIO UBICACIONES (REGISTRO)
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
    const formUbicacion = document.getElementById("form-ubicacion");
    const selectDepto = document.getElementById("ubicacion-departamento");
    const selectMunicipio = document.getElementById("ubicacion-municipio");

    if (selectDepto && selectMunicipio) {
        const grupos = Array.from(selectMunicipio.querySelectorAll("optgroup"));

        function filtrarMunicipios() {
            const depto = selectDepto.value;

            grupos.forEach((g) => (g.style.display = "none"));
            selectMunicipio.disabled = true;

            if (!depto) {
                selectMunicipio.value = "";
                return;
            }

            selectMunicipio.disabled = false;
            selectMunicipio.value = "";

            grupos.forEach((g) => {
                if (g.dataset.parent === depto) {
                    g.style.display = "block";
                }
            });
        }

        grupos.forEach((g) => (g.style.display = "none"));
        selectMunicipio.disabled = true;

        if (selectDepto.value) filtrarMunicipios();
        selectDepto.addEventListener("change", filtrarMunicipios);
    }

    if (formUbicacion) {
        formUbicacion.addEventListener("submit", (e) => {
            e.preventDefault();
            limpiarMensajes(formUbicacion);

            const depto = selectDepto.value.trim();
            const municipio = selectMunicipio.value.trim();
            const direccion = document
                .getElementById("ubicacion-direccion")
                .value.trim();

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
                marcarInvalido(
                    document.getElementById("ubicacion-direccion"),
                    "Ingrese una dirección más detallada."
                );
                valido = false;
            }

            if (valido) formUbicacion.submit();
            else mostrarAlerta("⚠ Corrige los campos marcados", "danger", formUbicacion);
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
        form.querySelectorAll(".is-invalid").forEach((el) =>
            el.classList.remove("is-invalid")
        );
        form.querySelectorAll(".invalid-feedback").forEach((el) => el.remove());
    }

    function mostrarAlerta(mensaje, tipo, form) {
        const alerta = document.createElement("div");
        alerta.className = `alert alert-${tipo} mt-3`;

        const container = form.closest(".card") || form;
        container.querySelectorAll(".alert").forEach((a) => a.remove());

        alerta.textContent = mensaje;
        container.prepend(alerta);
        setTimeout(() => alerta.remove(), 4000);
    }
});

// ============================================================
// GESTIÓN DE CONDUCTORES
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formConductor");
    const modalElement = document.getElementById("modalRegistroConductor");

    if (!form || !modalElement) return;

    const nombre = document.getElementById("nombre");
    const dui = document.getElementById("dui");
    const licencia = document.getElementById("licencia");
    const telefono = document.getElementById("telefono");
    const fechaVencimiento = document.getElementById("fechaVencimiento");

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
            let v = dui.value.replace(/\D/g, "").slice(0, 9);
            if (v.length > 8) v = v.slice(0, 8) + "-" + v.slice(8);
            dui.value = v;
        });
    }

    if (licencia) {
        licencia.addEventListener("input", () => {
            let v = licencia.value.replace(/\D/g, "").slice(0, 14);
            if (v.length > 4) v = v.slice(0, 4) + "-" + v.slice(4);
            if (v.length > 11) v = v.slice(0, 11) + "-" + v.slice(11);
            if (v.length > 15) v = v.slice(0, 15) + "-" + v.slice(15);
            licencia.value = v;
        });
    }

    if (telefono) {
        telefono.addEventListener("input", () => {
            let v = telefono.value.replace(/\D/g, "").slice(0, 8);
            if (v.length > 4) v = v.slice(0, 4) + "-" + v.slice(4);
            telefono.value = v;
        });
    }

    form.addEventListener("submit", (evt) => {
        evt.preventDefault();

        let valido = true;

        if (!/^\d{8}-\d$/.test(dui.value)) {
            dui.classList.add("is-invalid");
            valido = false;
        } else dui.classList.remove("is-invalid");

        if (!/^\d{4}-\d{6}-\d{3}-\d$/.test(licencia.value)) {
            licencia.classList.add("is-invalid");
            valido = false;
        } else licencia.classList.remove("is-invalid");

        if (!/^\d{4}-\d{4}$/.test(telefono.value)) {
            telefono.classList.add("is-invalid");
            valido = false;
        } else telefono.classList.remove("is-invalid");

        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);

        const fechaIngresada = new Date(fechaVencimiento.value);
        if (!fechaVencimiento.value || fechaIngresada < hoy) {
            fechaVencimiento.classList.add("is-invalid");
            valido = false;
        } else fechaVencimiento.classList.remove("is-invalid");

        form.classList.add("was-validated");

        if (valido) form.submit();
    });

    if (typeof bootstrap !== "undefined") {
        const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        modalElement.addEventListener("hidden.bs.modal", () => {
            form.reset();
            form.classList.remove("was-validated");
            form.querySelectorAll(".is-invalid").forEach((e) =>
                e.classList.remove("is-invalid")
            );
        });
    }
});

