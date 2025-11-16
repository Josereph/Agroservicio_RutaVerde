// 📌 CONTENIDO DE: static/js/preloader.js (SIN TIEMPO MÍNIMO)

(function() {
    var preloader = document.getElementById('preloader');
    
    // Si el elemento preloader no existe, no hacemos nada
    if (!preloader) return; 

    // Esta función se ejecutará cuando TODOS los recursos (imágenes, CSS, scripts, etc.)
    // de la ventana hayan terminado de cargarse.
    window.addEventListener('load', function() {
        
        // 1. Inicia la transición CSS de desaparición (opacidad a 0)
        preloader.classList.add('loaded');

        // 2. Espera el tiempo de la transición CSS (0.7 segundos) 
        // y luego elimina el elemento del DOM.
        // Esto libera recursos y evita que el preloader bloquee clics.
        setTimeout(function() {
            preloader.remove();
        }, 700); 
    });
})();