document.addEventListener('DOMContentLoaded', function() {
    console.log("El DOM ha sido cargado correctamente.");

    var calendarEl = document.getElementById('calendar');
    console.log("El elemento del calendario ha sido encontrado:", calendarEl);

    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuración del calendario...
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'today'
        },
        locale: 'es', // Configuración para el idioma español
         // the default (unnecessary to specify)
        
        events: {
            url: getHorariosClaseURL,
            method: 'GET',
            success: function(response) {
                console.log("Eventos cargados correctamente:", response);
            },
            failure: function(response) {
                console.error("Error al cargar eventos:", response);
            },
            

        },
    });

    calendar.render();
});
