jQuery(function() {
    $.datepicker.setDefaults($.extend({changeMonth:false, changeYear:false, dateFormat:'dd/mm/yy'},$.datepicker.regional['es']))
    /*$("#fecha-mobile").datepicker();*/
    /*$("input[type='submit']").click(function(e) {
        e.preventDefault();
        $.post("s.php", $("form").serializeArray(), function(message) {
            window.location="v.php" 
        });
    });*/
});

