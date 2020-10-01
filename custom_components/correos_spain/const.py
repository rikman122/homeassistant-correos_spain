"""Constants for the Correos Spain Tracking integration."""
import logging

DOMAIN = "correos_spain"
LOGGER = logging.getLogger(__name__)
CORREOS_API_TEMPLATE = "https://localizador.correos.es/canonico/eventos_envio_servicio/{0}?codAplicacion=60&codCanal=3&codIdioma=ES&indUltEvento=N"
UNIQUE_ID_TEMPLATE = "correos_spain_{0}"
ENTITY_ID_TEMPLATE = "sensor.correos_spain_package_{0}"
TITLE_TEMPLATE = "Tracking {0}"
ATTRIBUTION = "Data provided by correos.es"