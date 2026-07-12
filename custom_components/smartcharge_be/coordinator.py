"""Data update coordinator for SmartCharge BE."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CAR_BYD,
    CAR_OMODA,
    EASEE_CURRENT_ENTITY,
    MAX_CURRENT_BYD_ENTITY,
    MAX_CURRENT_OMODA_ENTITY,
    MAX_GRID_POWER_ENTITY,
    P1_POWER_ENTITY,
    SELECTED_CAR_ENTITY,
)

_LOGGER = logging.getLogger(__name__)

_INVALID_STATES = {"unknown", "unavailable", ""}

VOLTAGE_PER_PHASE = 230.0
MINIMUM_CHARGING_CURRENT = 6.0

EASEE_DOMAIN = "easee"
EASEE_SERVICE = "set_charger_dynamic_limit"
EASEE_DEVICE_ID = "e98abe937adc396a267e96c65f41e27f"

# Automatische aansturing blijft voorlopig uit.
AUTO_CONTROL_ENABLED = False


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

        self._last_sent_current: int | None = None

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
        """Read a text Home Assistant entity."""
        state = self.hass.states.get(entity_id)

        if state is None or state.state in _INVALID_STATES:
            return None

        return state.state

    async def _async_send_easee_limit(
        self,
        target_current: int,
    ) -> bool:
        """Send a dynamic charging limit to Easee."""
        if not AUTO_CONTROL_ENABLED:
            return False

        if self._last_sent_current == target_current:
            return False

        if not self.hass.services.has_service(
            EASEE_DOMAIN,
            EASEE_SERVICE,
        ):
            _LOGGER.warning(
                "Easee-service %s.%s is niet beschikbaar",
                EASEE_DOMAIN,
                EASEE_SERVICE,
            )
            return False

        try:
            await self.hass.services.async_call(
                EASEE_DOMAIN,
                EASEE_SERVICE,
                {
                    "device_id": EASEE_DEVICE_ID,
                    "current": target_current,
                },
                blocking=True,
            )
        except HomeAssistantError:
            _LOGGER.exception(
                "Instellen van Easee-laadstroom op %s A is mislukt",
                target_current,
            )
            return False

        self._last_sent_current = target_current

        _LOGGER.info(
            "Easee dynamische laadlimiet ingesteld op %s A",
            target_current,
        )

        return True

    async def _async_update_data(self) -> dict[str, Any]:
        """Read entities and calculate phase-aware charging values."""
        p1_power = self._read_number(P1_POWER_ENTITY)
        easee_current = self._read_number(EASEE_CURRENT_ENTITY)
        selected_car = self._read_text(SELECTED_CAR_ENTITY)
        max_grid_power = self._read_number(MAX_GRID_POWER_ENTITY)

        max_current_omoda = self._read_number(
            MAX_CURRENT_OMODA_ENTITY
        )
        max_current_byd = self._read_number(
            MAX_CURRENT_BYD_ENTITY
        )

        selected_max_current: float | None = None
        number_of_phases: int | None = None

        if selected_car == CAR_OMODA:
            selected_max_current = max_current_omoda
            number_of_phases = 1
        elif selected_car == CAR_BYD:
            selected_max_current = max_current_byd
            number_of_phases = 3

        current_charging_power: float | None = None
        house_power_without_charger: float | None = None
        allowed_charging_power: float | None = None
        available_current: float | None = None
        target_current: int | None = None

        if (
            p1_power is not None
            and easee_current is not None
            and max_grid_power is not None
            and number_of_phases is not None
        ):
            current_charging_power = (
                easee_current
                * VOLTAGE_PER_PHASE
                * number_of_phases
            )

            house_power_without_charger = (
                p1_power - current_charging_power
            )

            allowed_charging_power = max(
                0.0,
                max_grid_power - house_power_without_charger,
            )

            calculated_current = (
                allowed_charging_power
                / VOLTAGE_PER_PHASE
                / number_of_phases
            )

            if selected_max_current is not None:
                available_current = min(
                    calculated_current,
                    selected_max_current,
                )
            else:
                available_current = calculated_current

            available_current = max(0.0, available_current)

            if available_current < MINIMUM_CHARGING_CURRENT:
                target_current = 0
            else:
                target_current = int(available_current)

            if target_current is not None:
             await self._async_send_easee_limit(target_current)

        return {
            "p1_power": p1_power,
            "easee_current": easee_current,
            "selected_car": selected_car,
            "number_of_phases": number_of_phases,
            "max_grid_power": max_grid_power,
            "max_current_omoda": max_current_omoda,
            "max_current_byd": max_current_byd,
            "selected_max_current": selected_max_current,
            "current_charging_power": current_charging_power,
            "house_power_without_charger": house_power_without_charger,
            "allowed_charging_power": allowed_charging_power,
            "available_current": available_current,
            "target_current": target_current,
            "last_sent_current": self._last_sent_current,
        }