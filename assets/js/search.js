function search_submit() {
	var query = $("#id_keywords").val();
    var periodo = $("#fecha_periodo").val();
	$("#posts").empty();
    $("#posts").html('<img src="/static/images/ajax-loader.gif"> Buscando...');
	$("#posts").load(
			"/buscar/?ajax&query=" + encodeURIComponent(query) + "&fecha_periodo=" + encodeURIComponent(periodo)
	);
	return false;
}
$(document).ready(function () {
	$("#search-form").submit(search_submit);
})