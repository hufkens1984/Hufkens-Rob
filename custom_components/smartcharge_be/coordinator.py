"""Data update coordinator for SmartCharge BE."""

from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)


class SmartChargeCoordinator(DataUpdateCoordinator):
    """Coordinator for SmartCharge BE."""

    def __init__(self, hass):
        super().__init__(
            hass,
            logger=None,
            name="SmartCharge BE",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch data."""
        return {}
