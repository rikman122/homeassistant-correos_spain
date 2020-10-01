"""Config flow for Correos Spain Tracking integration."""
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, LOGGER, UNIQUE_ID_TEMPLATE, TITLE_TEMPLATE

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("tracking_number"): str,
        vol.Required("delete_delivered"): bool,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Correos Spain Tracking."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:

            await self.async_set_unique_id(
                UNIQUE_ID_TEMPLATE.format(user_input["tracking_number"])
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=TITLE_TEMPLATE.format(user_input["name"]), data=user_input
            )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
