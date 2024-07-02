var registrosalida = {
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
                { data: "id" },
                { data: "alumno.nombre_completo" },
                { data: "hora_salida" },
                { data: "fecha" },
                { data: "descripcion_actividad" },
                { data: "total_horas" },
                { data: "id" },
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-bs-toggle="tooltip" title="Editar" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-bs-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></a>';
                        return buttons;
                    }
                },
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
    registrosalida.list();
});
