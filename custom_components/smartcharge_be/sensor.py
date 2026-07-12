"""Sensor platform for SmartCharge BE."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SmartCharge BE sensors."""

    async_add_entities(
        [
            SmartChargeStatusSensor(entry),
        ]
    )


class SmartChargeStatusSensor(SensorEntity):
    """Simple test sensor for SmartCharge BE."""

    _attr_name = "SmartCharge BE status"
    _attr_native_value = "Actief"
    _attr_icon = "mdi:ev-station"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{entry.entry_id}_status"
