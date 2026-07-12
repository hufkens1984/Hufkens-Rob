"""Data update coordinator for SmartCharge BE."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CAR_BYD,
    CAR_OMODA,
    MAX_CURRENT_BYD_ENTITY,
    MAX_CURRENT_OMODA_ENTITY,
    MAX_GRID_POWER_ENTITY,
    P1_POWER_ENTITY,
    SELECTED_CAR_ENTITY,
)

_LOGGER = logging.getLogger(__name__)

_INVALID_STATES = {"unknown", "unavailable", ""}

VOLTAGE_PER_PHASE = 230.0
NUMBER_OF_PHASES = 3
MINIMUM_CHARGING_CURRENT = 6.0


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
        """Read entities and calculate charging values."""
        p1_power = self._read_number(P1_POWER_ENTITY)
        selected_car = self._read_text(SELECTED_CAR_ENTITY)
        max_grid_power = self._read_number(MAX_GRID_POWER_ENTITY)
        max_current_omoda = self._read_number(
            MAX_CURRENT_OMODA_ENTITY
        )
        max_current_byd = self._read_number(
            MAX_CURRENT_BYD_ENTITY
        )

        selected_max_current: float | None = None

        if selected_car == CAR_OMODA:
            selected_max_current = max_current_omoda
        elif selected_car == CAR_BYD:
            selected_max_current = max_current_byd

        available_power: float | None = None
        available_current: float | None = None
        target_current: int | None = None

        if p1_power is not None and max_grid_power is not None:
            available_power = max(
                0.0,
                max_grid_power - p1_power,
            )

            calculated_current = (
                available_power
                / VOLTAGE_PER_PHASE
                / NUMBER_OF_PHASES
            )

            if selected_max_current is not None:
                available_current = min(
                    calculated_current,
                    selected_max_current,
                )
            else:
                available_current = calculated_current

            available_current = max(
                0.0,
                available_current,
            )

            if available_current < MINIMUM_CHARGING_CURRENT:
                target_current = 0
            else:
                target_current = int(available_current)

        return {
            "p1_power": p1_power,
            "selected_car": selected_car,
            "max_grid_power": max_grid_power,
            "max_current_omoda": max_current_omoda,
            "max_current_byd": max_current_byd,
            "selected_max_current": selected_max_current,
            "available_power": available_power,
            "available_current": available_current,
            "target_current": target_current,
        }