var SPMaskBehavior = function (val) {
    return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
onKeyPress: function(val, e, field, options) {
    field.mask(SPMaskBehavior.apply({}, arguments), options);
    }
};


$(document).ready(function(){
    $('.mask-money').mask("#.##0,00", {reverse: true});

    $('.mask-phone').each(function () {
        let value = $(this).val();
        if (value.startsWith('+55')) {
            $(this).val(value.replace('+55', '').trim()); // Remove o +55
        }
    });

    $('.mask-phone').mask('(00) 00000-0000');

    $('.form').on('submit', function(){
        var valorComVirgula = $('.mask-money').val();
        var valorSemPonto = valorComVirgula.replace(/\./g, '');
        var valorCorreto = valorSemPonto.replace(',', '.');
        console.log(valorCorreto);
        $('.mask-money').val(valorCorreto);
    });

});