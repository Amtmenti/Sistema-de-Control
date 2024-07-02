var input_hora_entrada, input_fecha;

$(function () {
    // Inicializar campos de hora y fecha
    input_hora_entrada = $('input[name="hora_entrada"]');
    input_fecha = $('input[name="fecha"]');

    // Inicializar timepicker para la hora de entrada
    input_hora_entrada.datetimepicker({
        format: 'HH:mm',
        locale: 'es',
        keepOpen: false,
        defaultDate: moment()
    });

    // Inicializar datetimepicker para la fecha
    input_fecha.datetimepicker({
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

});
