"""Config flow for SmartCharge BE."""

from homeassistant import config_entries

from .const import DOMAIN


class SmartChargeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle first setup."""

        if user_input is not None:
            return self.async_create_entry(
                title="SmartCharge BE",
                data={},
            )

        return self.async_show_form(step_id="user")