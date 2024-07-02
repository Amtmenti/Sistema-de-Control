var input_hora_salida, input_fecha;

$(function () {
    // Inicializar campos de hora y fecha
    input_hora_salida = $('input[name="hora_salida"]');
    input_fecha = $('input[name="fecha"]');

    // Inicializar datetimepicker para la fecha
    input_fecha.datetimepicker({
        useCurrent: true,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: moment()
    });

    // Inicializar timepicker para la hora de salida
    input_hora_salida.datetimepicker({
        format: 'HH:mm',
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
