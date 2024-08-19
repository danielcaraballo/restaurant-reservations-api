
// sweet_alert.js
document.addEventListener("DOMContentLoaded", function() {
    // Ejemplo: mostrar una alerta SweetAlert2 al enviar un formulario en el panel de administración
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            Swal.fire({
                title: '¡Acción realizada!',
                text: 'El formulario se ha enviado exitosamente.',
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                form.submit();
            });
        });
    });
});