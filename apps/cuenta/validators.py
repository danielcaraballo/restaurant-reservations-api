import os
import requests
import json
import logging
from django.core.exceptions import ValidationError
from decouple import config
from requests.exceptions import RequestException

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def data_cedula(value):
    ORIGENES = ['V', 'E']
    CEDULA = value
    headers = {'Content-Type': 'application/json'}
    url_nomina = config('URL_NOMINA')
    url_saime = config('URL_SAIME')

    for origen in ORIGENES:
        try:
            response_nomina = requests.get(f"{url_nomina}nomina/trabajador/{origen}/{CEDULA}/", headers=headers, verify=False)
            response_nomina.raise_for_status()
        except RequestException as e:
            logger.error(f"Error al realizar la solicitud a nómina: {e}")
            continue

        if response_nomina.status_code == 200:
            try:
                response_saime = requests.get(f"{url_saime}{origen}/{CEDULA}/", headers=headers, verify=False)
                response_saime.raise_for_status()
            except RequestException as e:
                logger.error(f"Error al realizar la solicitud a SAIME: {e}")
                raise ValidationError('Error en la consulta al servicio SAIME')

            if response_saime.status_code == 200:
                try:
                    data = response_saime.json()
                    nom_ape = f"{data['primer_nombre']} {data.get('segundo_apellido', '')}"
                    return [nom_ape.strip(), origen]
                except (ValueError, KeyError) as e:
                    logger.error(f"Error al procesar la respuesta JSON: {e}")
                    raise ValidationError('Error en el formato de la respuesta del servicio SAIME')
    
    raise ValidationError('Trabajador no encontrado en la nómina')
