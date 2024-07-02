var registroEntradaSalida = {
    list: function () {
        $('#data').DataTable({
            autoWidth: true,
            destroy: true,
            deferRender: true,
            responsive: true,
            rowReorder: {
                selector: 'td:nth-child(2)'
            },
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search'
                },
                dataSrc: ""
            },
            columns: [
                { data: "alumno" },
                { data: "hora_entrada" },
                { data: "hora_salida" },
                { data: "fecha" },
                { data: "descripcion_actividad" },
                { data: "total_horas" }
            ],
            rowCallback: function (row, data, index) {
            },
            initComplete: function (settings, json) {
                enable_tooltip();
            }
        });
    }
};

$(function () {
    registroEntradaSalida.list();
});
