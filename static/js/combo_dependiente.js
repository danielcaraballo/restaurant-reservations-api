function getMunicipio(estado)
{
    let $ = django.jQuery;
    $.ajax({
                type: "GET",
                url: '/geo/municipios/filtro/'+estado+'/',
                dataType: "json",
                success: function(data)
                {
                    let lista = '<option value="" selected="">SELECCIONE</option>'

                    $.each(data, function(key, val)
                    {
                        lista += '<option value="'+ val.id +'">'+ val.nombre +'</option>'
                    });
                    $('#municipio').html(lista);
                }
            });
}

function getParroquia(municipio)
{
    let $ = django.jQuery;
    $.ajax({
            type: "GET",
            url: '/geo/parroquias/filtro/'+municipio+'/',
            dataType: "json",
            success: function(data)
            {
                let lista = '<option value="" selected="">SELECCIONE</option>'

                $.each(data, function(key, val)
                {
                    lista += '<option value="'+ val.id +'">'+ val.nombre +'</option>'
                });
                $('#parroquia').html(lista);
            }
        });
}
