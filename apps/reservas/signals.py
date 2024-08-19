from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.gestion.models.ingreso import Ingreso, IngresosBienes
from apps.gestion.models.lote import Lote
from apps.gestion.models.salida  import Salida, SalidasBienes 
from apps.gestion.models.almacen import Almacen
from django.contrib import messages



@receiver(pre_save, sender=Ingreso)
def incrementar_contador(sender, instance, **kwargs):
    # Verifica si el objeto Ingreso ya tiene un ID asignado, lo que indica que está siendo actualizado
    if instance.pk is None:
        # Consulta el último registro insertado
        ultimo_registro = Ingreso.objects.last()
        # Obtén el valor del contador del último registro insertado
        if ultimo_registro:
            ultimo_contador = ultimo_registro.contador
            # Verifica si el contador ha alcanzado 999 y restablécelo a 1
            if ultimo_contador >= 999:
                instance.contador = 1
            else:
                instance.contador = ultimo_contador + 1
        else:
            # Si no hay registros previos, establece el contador a 1
            instance.contador = 1

        # Formatea el código con el formato deseado
        if instance.contador < 10:
            contador_str = f"00{instance.contador}"
        elif instance.contador < 100:
            contador_str = f"0{instance.contador}"
        else:
            contador_str = str(instance.contador)
        
        # Genera el código utilizando la fecha y el contador
        instance.codigo = f"{instance.fecha.strftime('%d%m%Y')}-{contador_str}"

@receiver(post_save, sender=IngresosBienes)
def actualizar_almacen(sender, instance, created, **kwargs):
    if created:
        ingreso = instance.codigo_de_lote_id
        ultimo_lote = IngresosBienes.objects.filter(codigo_de_lote=ingreso).first()
        Lote.objects.create( bien=ultimo_lote.bien, cantidad=ultimo_lote.cantidad, codigo_de_lote_id=ingreso)
        try:
            almacen = Almacen.objects.get(bien=ultimo_lote.bien)
            almacen.cantidad += ultimo_lote.cantidad
            almacen.save()
        except Almacen.DoesNotExist:
            Almacen.objects.create(bien=ultimo_lote.bien, cantidad=ultimo_lote.cantidad)

@receiver(post_save, sender=SalidasBienes)
def restar_almacen(sender, instance, created, **kwargs):
    if created:
        codigo_lote = instance.codigo_de_lote_id
        ultimo_bien = SalidasBienes.objects.filter(codigo_de_lote=codigo_lote).first()
        almacen = Almacen.objects.get(bien=ultimo_bien.bien)
        lote = Lote.objects.get(bien=ultimo_bien.bien, codigo_de_lote_id=codigo_lote)
        try:
            if ultimo_bien.cantidad <= lote.cantidad:
                
                almacen.cantidad -= ultimo_bien.cantidad
                almacen.save()
               
                lote.cantidad -= ultimo_bien.cantidad
                lote.save()
            else:
                mensaje = f"La cantidad solicitada de {ultimo_bien.bien} no se encuentra en el almacén."
                #messages.error(instance, mensaje)
                raise ValueError(mensaje)
            
        except Almacen.DoesNotExist:
            # El objeto Almacen no existe
            mensaje = f"El bien {ultimo_bien.bien} no existe en el almacén."
            # Puedes mostrar este mensaje de alguna manera adecuada, como imprimirlo en la consola o pasarlo a una plantilla HTML si estás trabajando en una aplicación web
            print(mensaje)
            # O puedes lanzar una excepción personalizada si lo prefieres
            raise ValueError(mensaje)

