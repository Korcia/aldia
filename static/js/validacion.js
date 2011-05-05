jQuery(function(){
        $("#searchsubmit").click(function(){
        $("#errores").empty();
        var hasError = false;
        var searchReg = /^[a-zA-Z0-9-\s]+$/;
        var searchVal = $("#id_keywords").val();
        if(searchVal == '') {
            $("#errores").append('<span class="error">Por favor, introduzca una palabra.</span>');
            $("#errores").show();
            hasError = true;
        } else if(!searchReg.test(searchVal)) {
            $("#errores").append('<span class="error">Introduzca letras y/o números.</span>');
            $("#errores").show();
            hasError = true;
        }
        if(hasError == true) {return false;}
    });
});