$(document).ready(function() {
    $('#modele').on('change', function() {
        $('.data').hide();
        $('#' + $(this).val()).fadeIn(700);
    }).change();
});