"""Sensor platform for SmartCharge BE."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import Event, EventStateChangedData, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import P1_POWER_ENTITY


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SmartCharge BE sensors."""

    async_add_entities(
        [
            SmartChargeStatusSensor(entry),
            SmartChargeP1PowerSensor(hass, entry),
        ]
    )


class SmartChargeStatusSensor(SensorEntity):
    """Status sensor for SmartCharge BE."""

    _attr_name = "SmartCharge BE status"
    _attr_native_value = "Actief"
    _attr_icon = "mdi:ev-station"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{entry.entry_id}_status"


class SmartChargeP1PowerSensor(SensorEntity):
    """Show the current P1 meter power."""

    _attr_name = "SmartCharge P1 vermogen"
    _attr_icon = "mdi:flash"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._attr_unique_id = f"{entry.entry_id}_p1_power"
        self._attr_native_value = None
        self._remove_listener = None

    async def async_added_to_hass(self) -> None:
        """Start listening for P1 meter updates."""
        await super().async_added_to_hass()

        self._update_from_source()

        self._remove_listener = async_track_state_change_event(
            self.hass,
            [P1_POWER_ENTITY],
            self._handle_source_change,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Stop listening when the sensor is removed."""
        if self._remove_listener is not None:
            self._remove_listener()

        await super().async_will_remove_from_hass()

    def _handle_source_change(
        self,
        event: Event[EventStateChangedData],
    ) -> None:
        """Handle a change of the P1 source sensor."""
        self._update_from_source()
        self.async_write_ha_state()

    def _update_from_source(self) -> None:
        """Read the current P1 meter value."""
        source_state = self.hass.states.get(P1_POWER_ENTITY)

        if source_state is None or source_state.state in {
            "unknown",
            "unavailable",
        }:
            self._attr_native_value = None
            return

        try:
            self._attr_native_value = float(source_state.state)
        except ValueError:
            self._attr_native_value = None