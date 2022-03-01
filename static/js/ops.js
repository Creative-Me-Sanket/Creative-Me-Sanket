
$('li a').click(function(e) {
    e.preventDefault();
    $('a').removeClass('mm-active');
    $(this).addClass('mm-active');
});

function replaceDiv(divId) {
    document.getElementById('dashcontainer').innerHTML = document.getElementById(divId).innerHTML;
}