"""Sensor platform for the Coreos Spain Post Service."""
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity
from homeassistant.helpers import aiohttp_client
import ssl
import asyncio
import aiohttp
import async_timeout

from .const import (
    LOGGER,
    UNIQUE_ID_TEMPLATE,
    ENTITY_ID_TEMPLATE,
    CORREOS_API_TEMPLATE,
    ATTRIBUTION,
)
from datetime import timedelta

SCAN_INTERVAL = timedelta(minutes=15)

ICON = "mdi:cube-send"

ATTR_EVENT = "event"
ATTR_DESCRIPTION = "description"
ATTR_DATE = "date"
ATTR_TIME = "time"
ATTR_TRACKING_NUMBER = "tracking_number"
ATTR_FRIENDLY_NAME = "friendly_name"
ATTR_LOCATION = "location"

EVENT_CODE_DELIVERED = "I010000V"
EVENT_CODE_IN_DELIVERY = "H020000V"
EVENT_CODE_IN_DELIVERY_UNIT = "G01L010V"
EVENT_CODE_CLASIFIED = "P040000V"
EVENT_CODE_ADMITTED = "A010000V"
EVENT_CODE_REGISTERED = "A090000V"

NOTIFICATION_DELIVERY_ID = "correos_package_in_delivery_{0}"
NOTIFICATION_DELIVERY_TITLE = "Paquete en reparto"
NOTIFICATION_DELIVERY_MESSAGE = "El paquete {0} está en reparto"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    client = aiohttp_client.async_get_clientsession(hass)

    async_add_entities(
        [
            CorreosSpainPackageSensor(
                client,
                config_entry.data["name"],
                config_entry.data["tracking_number"],
                config_entry.data["delete_delivered"],
            )
        ],
        True,
    )


class CorreosSpainPackageSensor(Entity):
    """Sensor representing package data."""

    def __init__(self, client, name, tracking_number, delete_delivered):
        """Initialize package sensor."""
        self.client = client
        self._attrs = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_FRIENDLY_NAME: name,
            ATTR_TRACKING_NUMBER: tracking_number,
            ATTR_EVENT: None,
            ATTR_DESCRIPTION: None,
            ATTR_LOCATION: None,
            ATTR_DATE: None,
            ATTR_TIME: None,
        }
        self._friendly_name = name
        self._state = None
        self._tracking_number = tracking_number
        self._event_code = None
        self._delete_delivered = delete_delivered
        self._already_notified = False
        self.entity_id = ENTITY_ID_TEMPLATE.format(self._tracking_number)

    @property
    def available(self):
        """Return if sensor is available."""
        return self._state is not None

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        return self._attrs

    @property
    def icon(self):
        """Return the icon."""
        return ICON

    @property
    def name(self):
        """Return the name."""
        return f"{self._friendly_name} - {self._tracking_number}"

    @property
    def state(self):
        """State of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return UNIQUE_ID_TEMPLATE.format(self._tracking_number)

    async def async_update(self):
        """Updates the tracking information"""
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.set_ciphers("DEFAULT@SECLEVEL=1")

            async with async_timeout.timeout(10):
                response = await self.client.get(
                    CORREOS_API_TEMPLATE.format(self._tracking_number), ssl=context
                )

                tracking_info = await response.json()
                error = tracking_info[0]["error"]

                if error["codError"] != "0":
                    self._state = "Unknown"
                    self._attrs[ATTR_DESCRIPTION] = error["desError"]
                    self._event_code = error["codError"]
                    return

                else:
                    last_event = tracking_info[0]["eventos"][-1]
                    self._event_code = last_event["codEvento"]
                    self._state = last_event["desTextoResumen"]
                    self._attrs[ATTR_EVENT] = last_event["desTextoResumen"]
                    self._attrs[ATTR_DESCRIPTION] = last_event["desTextoAmpliado"]
                    self._attrs[ATTR_LOCATION] = last_event["unidad"]
                    self._attrs[ATTR_DATE] = last_event["fecEvento"]
                    self._attrs[ATTR_TIME] = last_event["horEvento"]

        except (asyncio.TimeoutError, aiohttp.ClientError):
            self._state = "Error"
            self._attrs[ATTR_DESCRIPTION] = "Something went wrong updating the state"
            self._event_code = "-1"
            return

        if self._event_code == EVENT_CODE_DELIVERED and self._delete_delivered:
            self.hass.async_create_task(self._remove())
            return

        if self._event_code == EVENT_CODE_IN_DELIVERY and not self._already_notified:
            self._notify_in_delivery()

    async def _remove(self):
        """Remove entity itself."""
        await self.async_remove()

        reg = await self.hass.helpers.entity_registry.async_get_registry()
        entity_id = reg.async_get_entity_id(
            "sensor",
            "correos_spain",
            UNIQUE_ID_TEMPLATE.format(self._tracking_number),
        )
        if entity_id:
            reg.async_remove(entity_id)

    def _notify_in_delivery(self):
        """Notify when package is in delivery process"""
        identification = (
            self._friendly_name if self._friendly_name else self._tracking_number
        )
        message = NOTIFICATION_DELIVERY_MESSAGE.format(identification)
        title = NOTIFICATION_DELIVERY_TITLE.format(identification)
        notification_id = NOTIFICATION_DELIVERY_ID.format(self._tracking_number)

        self.hass.components.persistent_notification.create(
            message, title=title, notification_id=notification_id
        )

        self._already_notified = True