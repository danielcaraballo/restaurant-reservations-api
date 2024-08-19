from django.http import JsonResponse
from apps.gestion.models.ingreso import Ingreso, IngresosBienes


def filtrar_codigos_lote(request, bien_id):
    ingresos_bienes = IngresosBienes.objects.filter(bien_id=bien_id)
    codigos_lotes = []
    for ingreso in ingresos_bienes:
        id_ingreso = ingreso.codigo_de_lote_id
        codigos_lotes.extend(Ingreso.objects.filter(id=id_ingreso))

    data = [{'id': codigo_lote.id, 'codigo_de_lote': codigo_lote.codigo} for codigo_lote in codigos_lotes]
    return JsonResponse({'results': data})