var input_hentrada, input_hsalida;

$(function () {
    input_hentrada = $('input[name="hentrada"]');
    input_hsalida = $('input[name="hsalida"]');

    input_hentrada.datetimepicker({
        useCurrent: false,
        format: 'HH:mm',
        locale: 'es',
        keepOpen: false
    });

    input_hsalida.datetimepicker({
        useCurrent: false,
        format: 'HH:mm',
        locale: 'es',
        keepOpen: false
    });


    $('.select2').select2({
        language: 'es',
        theme: 'bootstrap4'
    });
    
});

