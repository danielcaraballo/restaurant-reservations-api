function getCodigoLote(bien) {
    let $ = django.jQuery;
    $.ajax({
        type: "GET",
        url: '/salidasbienes/filtro/' + bien + '/',  // Ruta de la vista que filtra los códigos de lote por bien
        dataType: "json",
        success: function(data) {
            console.log(data);
            let lista = '<option value="" selected="">SELECCIONE</option>';
            $.each(data['results'], function(key, val) {
               
                lista += '<option value="' + val.id + '">' + val.codigo_de_lote + '</option>';  // Asumiendo que el JSON devuelto contiene el campo 'codigo_de_lote' para el nombre del código de lote
            });
            $('#codigo_de_lote').html(lista);  // Actualiza las opciones del campo de código de lote en el formulario
        }
    });
}
