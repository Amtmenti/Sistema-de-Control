var input_alumno;
var current_date;
var tblReport;
var columns = [];
var report = {
    initTable: function () {
        tblReport = $('#tblReport').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            responsive: true,
            rowReorder: {
                selector: 'td:nth-child(2)'
            },
        });
        tblReport.settings()[0].aoColumns.forEach(function (value, index, array) {
            columns.push(value.sWidthOrig);
        });
    },
    list: function () {
        var parameters = {
            'action': 'search_report',
            'alumno': input_alumno.val(),
        };
        tblReport = $('#tblReport').DataTable({
            destroy: true,
            autoWidth: false,
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
                data: parameters,
                dataSrc: function (json) {
                    if (json.error) {
                        alert('Error: ' + json.error);
                        return [];
                    }
                    return json;
                },
                error: function (xhr, error, thrown) {
                    alert('Error en la petición Ajax: ' + xhr.status + ' ' + thrown);
                }
            },
            order: [[0, 'asc']],
            paging: false,
            ordering: true,
            searching: false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: ' <i class="fas fa-file-excel"></i> Descargar',
                    titleAttr: 'Excel',
                    className: 'btn btn-success btn-sm mb-3'
                }
            ],
            columns: [
                {data: "alumno.nombre_completo"},
                {data: "fecha"},
                {data: "hora_entrada"},
                {data: "hora_salida"},
                {data: "descripcion_actividad"},
                {data: "total_horas"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {

            }
        });
    }
};

$(function () {
    current_date = new moment().format('YYYY-MM-DD');
    input_alumno = $('select[name="alumno"]');

    input_alumno.on('change', function () {
        report.list();
    });

    report.initTable();

    report.list();
});
