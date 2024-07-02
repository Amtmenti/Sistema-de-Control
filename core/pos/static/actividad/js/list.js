var actividad = {
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
                { data: "nombre" },
                { data: "descripcion" },
                { data: "created_at" },
                { data: "email_status" },
                { data: "id"},
            ],
            columnDefs: [
                {
                    targets: -1,
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-bs-toggle="tooltip" title="Editar" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-bs-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></a>';
                        return buttons;
                    }
                },
                {
                    targets: 5,
                    className: 'text-center',
                    render: function (data, type, row) {
                        if (data === 'Exitoso') {
                            return '<span class="badge bg-success">Enviado</span>';
                        } else if (data === 'Fallido') {
                            return '<span class="badge bg-danger">Error, no enviado</span>';
                        } else {
                            return '<span class="badge bg-secondary">Desconocido</span>';
                        }
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
    actividad.list();
});
