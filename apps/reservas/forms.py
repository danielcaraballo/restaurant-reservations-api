from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from apps.gestion.models.ingreso import Ingreso, IngresosBienes
from apps.gestion.models.salida import SalidasBienes
from apps.auxiliares.models.bien import Bien
from apps.auxiliares.models.responsable import Responsable
from apps.auxiliares.models.motivo              import Motivo
from apps.auxiliares.models.responsable         import Responsable
from apps.geo.models.estados                    import Estados
from apps.geo.models.municipios                 import Municipios
from apps.geo.models.parroquias                 import Parroquias

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = '__all__'
        widgets = {
            'codigo': forms.HiddenInput(),
            'id_ingreso': forms.HiddenInput(),
            'contador': forms.HiddenInput(),
            'hoy': forms.HiddenInput(),
            'mes': forms.HiddenInput(),
            'anio': forms.HiddenInput()


        }

    def __init__(self,*args, **kwargs):
        super(IngresoForm, self).__init__(*args, **kwargs)

        motivo_lista = [('', '---------')] + [(columna.id, columna.motivo) for columna in Motivo.objects.exclude(tipo='SALIDA').all()]

        self.fields['motivo'].widget = forms.Select(
                choices=motivo_lista,
            )

        try:
            self.initial['estado'] = kwargs['instance'].estado.id
        except:
            pass
        
        estado_lista = [('', '---------')] + [(columna.id, columna.nombre) for columna in Estados.objects.all()]

        # try:
        #     self.initial['municipio'] = kwargs['instance'].municipio.id
        #     lista_municipios = [(columna.id, columna.nombre) for columna in Municipios.objects.filter(estado = kwargs['instance'].estado)]
        # except:
        #     lista_municipios = [('', '---------')]

        # try:
        #     self.initial['parroquia'] = kwargs['instance'].parroquia.id
        #     lista_parroquias = [(columna.id, columna.descripcion) for columna in Parroquias.objects.filter(municipio = kwargs['instance'].municipio)]
        # except:
        #     lista_parroquias = [('', '---------')]

        
        # self.fields['estado'].widget = forms.Select(
        #     attrs={
        #         'id':       'estado',
        #         'onchange': 'getMunicipio(this.value)',
        #         'style':    'width:200px'
        #     },
        #     choices=estado_lista,
        # )
        # self.fields['municipio'].widget = forms.Select(
        #     attrs={
        #         'id':       'municipio',
        #         'onchange': 'getParroquia(this.value)',
        #         'style':    'width:200px'
        #     },
        #     choices=lista_municipios
        # )
        # self.fields['parroquia'].widget = forms.Select(
        #     attrs={
        #         'id':       'parroquia',
        #         'onchange': 'getcomunidad(this.value)',
        #         'style':    'width:200px'
        #     },
        #     choices=lista_parroquias
        # )

        
class SalidaForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = '__all__'
        widgets = {
            'hoy': forms.HiddenInput(),
            'mes': forms.HiddenInput(),
            'anio': forms.HiddenInput()
        }

    def __init__(self,*args, **kwargs):
        super(SalidaForm, self).__init__(*args, **kwargs)

        motivo_lista = [('', '---------')] + [(columna.id, columna.motivo) for columna in Motivo.objects.exclude(tipo='INGRESO').all()]

        self.fields['motivo'].widget = forms.Select(
                choices=motivo_lista,
            )
        
        #try:
        #    self.initial['estado'] = kwargs['instance'].estado.id
        #except:
        #    pass
        #
        #estado_lista = [('', 'SELECCIONE')] + [(columna.id, columna.nombre) for columna in Estados.objects.all()]

        # try:
        #     self.initial['municipio'] = kwargs['instance'].municipio.id
        #     lista_municipios = [(columna.id, columna.nombre) for columna in Municipios.objects.filter(estado = kwargs['instance'].estado)]
        # except:
        #     lista_municipios = [('', '---------')]

        # try:
        #     self.initial['parroquia'] = kwargs['instance'].parroquia.id
        #     lista_parroquias = [(columna.id, columna.descripcion) for columna in Parroquias.objects.filter(municipio = kwargs['instance'].municipio)]
        # except:
        #     lista_parroquias = [('', '---------')]

        
        # self.fields['estado'].widget = forms.Select(
        #     attrs={
        #         'id':       'estado',
        #         'onchange': 'getMunicipio(this.value)',
        #         'style':    'width:200px'
        #     },
        #     choices=estado_lista,
        # )
        # self.fields['municipio'].widget = forms.Select(
        #     attrs={
        #         'id':       'municipio',
        #         'onchange': 'getParroquia(this.value)',
        #         'style':    'width:200px'
        #     },
        #     choices=lista_municipios
        # )
        # self.fields['parroquia'].widget = forms.Select(
        #     attrs={
        #         'id':       'parroquia',
        #         'onchange': 'getcomunidad(this.value)',
        #         'style':    'width:200px'
        #     },
        #     choices=lista_parroquias
        # )

        self.fields['destinatario'].queryset = Responsable.objects.filter(tipo='Destinatario')
        self.fields['jefe_de_almacen'].queryset = Responsable.objects.filter(tipo='Almacén')
        self.fields['supervisor_de_seguridad'].queryset = Responsable.objects.filter(tipo='Seguridad')
        self.fields['transportista'].queryset = Responsable.objects.filter(tipo='Transportista')

        

class SalidasBienesForm(forms.ModelForm):
    class Meta:
        model = SalidasBienes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SalidasBienesForm, self).__init__(*args, **kwargs)

        bien_lista = [('', 'SELECCIONE')] + [(bien.id, bien.bien) for bien in Bien.objects.all()]
        lista_codigos_lote = [('', 'SELECCIONE')]
        
        if self.instance.pk:  # Verifica si existe una instancia del objeto
            lista_codigos_lote = [(IngresoBien.id, IngresoBien.codigo_de_lote) for IngresoBien in IngresosBienes.objects.filter(bien=self.instance.bien)]
                 
        self.fields['bien'].widget = forms.Select(
            attrs={
                'id': 'bien',
                'onchange': 'getCodigoLote(this.value)',
                'style': 'width:200px'
            },
            choices=bien_lista,
        )

        self.fields['codigo_de_lote'].widget = forms.Select(
            attrs={
                'id': 'codigo_de_lote',
                'style': 'width:200px'
            },
            choices=lista_codigos_lote,
        )



    
