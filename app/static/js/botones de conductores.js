document.addEventListener('DOMContentLoaded', () => {
    
  
    // 1. REFERENCIAS AL DOM
  
    const form = document.getElementById('formConductor');
    const modalElement = document.getElementById('modalRegistroConductor');
    const modalInstance = new bootstrap.Modal(modalElement); 
    const btnGuardar = form.querySelector('button[type="submit"]');
    const tituloModal = document.getElementById('modalLabel');
    
    // Filtros
    const inputBusqueda = document.querySelector('input[placeholder="Buscar por nombre o documento..."]');
    const selectFiltroEstado = document.querySelector('select.form-select'); // El select de arriba (filtros)

  
    // 2. VALIDACIÓN Y ENVÍO
 
    form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });

   
    // 3. LIMPIEZA DEL MODAL (RESET AL CERRAR)
   
    modalElement.addEventListener('hidden.bs.modal', () => {
        form.reset();
        form.classList.remove('was-validated');
        
        // Restaurar textos por defecto (por si se usó "Editar")
        tituloModal.textContent = 'Registrar Nuevo Conductor';
        btnGuardar.innerHTML = '<i class="bi bi-save-fill me-2"></i> Guardar Conductor';
        
        // Resetear selects manualmente si es necesario
        document.getElementById('estado').value = 'Activo';
    });


    // 4. BOTÓN "EDITAR" (Cargar datos de la tabla al modal)
    
    const tablaBody = document.getElementById('tablaConductoresBody');

    tablaBody.addEventListener('click', (e) => {
        // Detectar si el clic fue en el botón de editar (o su icono)
        const btnEditar = e.target.closest('button[title="Editar"]');
        
        if (btnEditar) {
            const fila = btnEditar.closest('tr');
            
            // Obtener datos de las columnas (0=Nombre, 1=DUI, 2=Licencia, 3=Tel, 4=Email, 5=Estado)
            const nombre = fila.cells[0].textContent.trim();
            const documento = fila.cells[1].textContent.trim();
            const tipoLicencia = fila.cells[2].textContent.trim();
            const telefono = fila.cells[3].textContent.trim();
            const correo = fila.cells[4].textContent.trim();
            const estadoTexto = fila.cells[5].textContent.trim(); 

            // Llenar el formulario
            document.getElementById('nombre').value = nombre;
            document.getElementById('dui').value = documento;
            document.getElementById('tipoLicencia').value = tipoLicencia;
            
            // Limpiar guiones si vienen vacíos "—"
            document.getElementById('telefono').value = (telefono === '—') ? '' : telefono;
            document.getElementById('correo').value = (correo === '—') ? '' : correo;

            // Mapear Estado
            const selectEstado = document.getElementById('estado');
            // Buscar la opción que coincida con el texto
            for (let i = 0; i < selectEstado.options.length; i++) {
                if (selectEstado.options[i].text.includes(estadoTexto)) {
                    selectEstado.selectedIndex = i;
                    break;
                }
            }

            // Cambiar interfaz a "Modo Edición"
            tituloModal.textContent = 'Editar Conductor';
            btnGuardar.innerHTML = '<i class="bi bi-pencil-square me-2"></i> Actualizar';
            
            // Abrir el modal
            modalInstance.show();
        }
    });

  
    // 5. BOTÓN "ELIMINAR"
  
    tablaBody.addEventListener('click', (e) => {
        const btnEliminar = e.target.closest('button[title="Eliminar"]');
        
        if (btnEliminar) {
            // En una app real, aquí tomarías el ID del conductor para enviar al backend
            if (confirm('¿Estás seguro de eliminar este conductor?')) {
                // Simulación visual de eliminación
                btnEliminar.closest('tr').remove();
                // Aquí harías: window.location.href = `/eliminar/${id}`;
            }
        }
    });

   
    // 6. FILTROS DE BÚSQUEDA (CLIENT-SIDE)
  
    function filtrarTabla() {
        const texto = inputBusqueda.value.toLowerCase();
        const estado = selectFiltroEstado.value;
        const filas = tablaBody.getElementsByTagName('tr');

        for (let fila of filas) {
            // Si es la fila de "No hay registros", la saltamos
            if (fila.cells.length < 2) continue;

            const nombre = fila.cells[0].textContent.toLowerCase();
            const dui = fila.cells[1].textContent.toLowerCase();
            const estadoFila = fila.cells[5].textContent.trim();

            const coincideTexto = nombre.includes(texto) || dui.includes(texto);
            const coincideEstado = estado === "" || estadoFila === estado;

            if (coincideTexto && coincideEstado) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        }
    }

    // Eventos para filtrar
    inputBusqueda.addEventListener('keyup', filtrarTabla);
    selectFiltroEstado.addEventListener('change', filtrarTabla);
});