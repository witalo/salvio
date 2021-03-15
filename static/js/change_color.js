if (sessionStorage.getItem('mode') === 'dark') {
    $('body').css({'filter': 'invert(1)'});
    $('input[id=opcion1]').prop('checked', true);
} else {
    $('input[id=opcion1]').prop('checked', false);
}

$('input[id=opcion1]').change(function () {
    if (this.checked) {

        $('body').css({'filter': 'invert(1)'})
        sessionStorage.setItem('mode', 'dark');
    } else {
        $('body').css({'filter': 'invert(0)'})
        sessionStorage.setItem('mode', 'white');
    }
});
