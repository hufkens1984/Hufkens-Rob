"""Data update coordinator for SmartCharge BE."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    MAX_CURRENT_BYD_ENTITY,
    MAX_CURRENT_OMODA_ENTITY,
    MAX_GRID_POWER_ENTITY,
    P1_POWER_ENTITY,
    SELECTED_CAR_ENTITY,
)

_LOGGER = logging.getLogger(__name__)

_INVALID_STATES = {"unknown", "unavailable", ""}


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

    def _read_number(self, entity_id: str) -> float | None:
        """Read a numeric Home Assistant entity."""
        state = self.hass.states.get(entity_id)

        if state is None or state.state in _INVALID_STATES:
            return None

        try:
            return float(state.state)
        except (TypeError, ValueError):
            _LOGGER.warning(
                "Ongeldige numerieke waarde voor %s: %s",
                entity_id,
                state.state,
            )
            return None

    def _read_text(self, entity_id: str) -> str | None:
        """Read a text-based Home Assistant entity."""
        state = self.hass.states.get(entity_id)

        if state is None or state.state in _INVALID_STATES:
            return None

        return state.state

    async def _async_update_data(self) -> dict[str, Any]:
        """Read the required Home Assistant entities."""
        return {
            "p1_power": self._read_number(P1_POWER_ENTITY),
            "selected_car": self._read_text(SELECTED_CAR_ENTITY),
            "max_grid_power": self._read_number(MAX_GRID_POWER_ENTITY),
            "max_current_omoda": self._read_number(
                MAX_CURRENT_OMODA_ENTITY
            ),
            "max_current_byd": self._read_number(
                MAX_CURRENT_BYD_ENTITY
            ),
        }