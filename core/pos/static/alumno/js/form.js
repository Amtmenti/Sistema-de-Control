var input_periodo_inicio, input_periodo_termino;

$(function () {
    // Inicializar input_periodos y horarios
    input_periodo_inicio = $('input[name="periodo_inicio"]');
    input_periodo_termino = $('input[name="periodo_termino"]');
    
    // Periodos
    input_periodo_inicio.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    input_periodo_termino.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    // Inicializar select2
    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4'
    });

    // Validación de nombre (solo letras)
    $('input[name="nombre_completo"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'letters'});
    });

    // Validación de teléfono (solo números)
    $('input[name="telefono_celular"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    // Validación de email (solo correos)
    $('input[name="email"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'email'});
    });
});
