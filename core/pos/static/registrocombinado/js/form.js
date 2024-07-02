$(function () {
    // Inicializar campos de hora y fecha
    $('input[name="hora_entrada"]').datetimepicker({
        format: 'HH:mm',
        locale: 'es',
        keepOpen: false,
        defaultDate: moment()
    });

    $('input[name="hora_salida"]').datetimepicker({
        format: 'HH:mm',
        locale: 'es',
        keepOpen: false,
        defaultDate: moment()
    });

    $('input[name="fecha"]').datetimepicker({
        useCurrent: true,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: moment()
    });

    // Inicializar select2
    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4'
    });

    // Validación de token (alfanúmerico)
    $('input[name="token"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'alphanumeric'});
    });

});
