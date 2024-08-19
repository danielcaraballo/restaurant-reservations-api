function getSubCategoria(categoria) {
    let $ = django.jQuery;
    $.ajax({
        type: "GET",
        url: '/subcategoria/filtro/' + categoria + '/',  // Ruta de la vista que filtra las subcategorías por categoría
        dataType: "json",
        success: function(data) {
            let lista = '<option value="" selected="">SELECCIONE</option>';
            $.each(data['results'], function(key, val) {
                lista += '<option value="' + val.id + '">' + val.subcategoria + '</option>';  // Asumiendo que el JSON devuelto contiene el campo 'subcategoria' para el nombre de la subcategoría
            });
            $('#subcategoria').html(lista);  // Actualiza las opciones del campo de subcategoría en el formulario
        }
    });
}