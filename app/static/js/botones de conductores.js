// Espera a que todo el contenido de la página esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. MANEJO DEL FORMULARIO DE REGISTRO ---
    
    // Seleccionamos el formulario por su ID
    const form = document.getElementById('formConductor');
    
    // Si este formulario no existe en la página, no hacemos nada más.
    if (!form) {
        return;
    }

    // Escuchamos el evento 'submit' (cuando el usuario hace clic en "Guardar Conductor")
    form.addEventListener('submit', (event) => {
        
        // Comprobamos si el formulario es válido (revisa los 'required', 'type="email"', etc.)
        if (!form.checkValidity()) {
            // Si NO es válido:
            // a. Prevenimos que el formulario se envíe al servidor
            event.preventDefault();
            event.stopPropagation();
        }
        
        // b. Aplicamos las clases de Bootstrap para mostrar los mensajes de error
        // (los "Por favor ingrese..." en rojo)
        // Si el formulario SÍ es válido, se envía al servidor como un POST normal.
        form.classList.add('was-validated');
    });

    // --- 2. (OPCIONAL PERO RECOMENDADO) LIMPIAR EL MODAL AL CERRAR ---
    
    // Buscamos el modal
    const modal = document.getElementById('modalRegistroConductor');
    
    if (modal) {
        // Escuchamos el evento 'hidden.bs.modal' (cuando el modal se ha terminado de ocultar)
        modal.addEventListener('hidden.bs.modal', () => {
            
            // a. Quitamos los estilos de validación (rojo/verde)
            form.classList.remove('was-validated');
            
            // b. Reseteamos todos los campos del formulario
            form.reset();
        });
    }
});