"""Data update coordinator for SmartCharge BE."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import P1_POWER_ENTITY

_LOGGER = logging.getLogger(__name__)


class SmartChargeCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for SmartCharge BE."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name="SmartCharge BE",
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Read data from Home Assistant entities."""
        p1_state = self.hass.states.get(P1_POWER_ENTITY)

        p1_power: float | None = None

        if (
            p1_state is not None
            and p1_state.state not in {"unknown", "unavailable"}
        ):
            try:
                p1_power = float(p1_state.state)
            except (TypeError, ValueError):
                _LOGGER.warning(
                    "Ongeldige waarde voor %s: %s",
                    P1_POWER_ENTITY,
                    p1_state.state,
                )

        return {
            "p1_power": p1_power,
        }