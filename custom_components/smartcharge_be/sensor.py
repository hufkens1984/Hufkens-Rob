"""Sensor platform for SmartCharge BE."""

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricCurrent, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SmartChargeCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SmartCharge BE sensors."""

    coordinator: SmartChargeCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            SmartChargeStatusSensor(coordinator, entry),
            SmartChargeP1PowerSensor(coordinator, entry),
            SmartChargeSelectedCarSensor(coordinator, entry),
            SmartChargeAvailableCurrentSensor(coordinator, entry),
            SmartChargeEaseeCurrentSensor(coordinator, entry),
            SmartChargeTargetCurrentSensor(coordinator, entry),
            SmartChargePhaseCountSensor(coordinator, entry),
            SmartChargeHousePowerSensor(coordinator, entry),
        ]
    )


class SmartChargeBaseSensor(
    CoordinatorEntity[SmartChargeCoordinator],
    SensorEntity,
):
    """Base class for SmartCharge BE sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the base sensor."""
        super().__init__(coordinator)
        self._entry = entry


class SmartChargeStatusSensor(SmartChargeBaseSensor):
    """Status sensor for SmartCharge BE."""

    _attr_name = "Status"
    _attr_icon = "mdi:ev-station"

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the status sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def native_value(self) -> str:
        """Return the integration status."""
        return "Actief"


class SmartChargeP1PowerSensor(SmartChargeBaseSensor):
    """Show the current P1 meter power."""

    _attr_name = "P1 vermogen"
    _attr_icon = "mdi:flash"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the P1 power sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_p1_power"

    @property
    def native_value(self) -> float | None:
        """Return the current P1 power."""
        value: Any = self.coordinator.data.get("p1_power")

        if isinstance(value, (int, float)):
            return float(value)

        return None


class SmartChargeSelectedCarSensor(SmartChargeBaseSensor):
    """Show the selected car."""

    _attr_name = "Geselecteerde auto"
    _attr_icon = "mdi:car-electric"

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the selected-car sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_selected_car"

    @property
    def native_value(self) -> str | None:
        """Return the selected car."""
        value: Any = self.coordinator.data.get("selected_car")

        if isinstance(value, str):
            return value

        return None


class SmartChargeAvailableCurrentSensor(SmartChargeBaseSensor):
    """Show the available charging current."""

    _attr_name = "Beschikbare laadstroom"
    _attr_icon = "mdi:current-ac"
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the available-current sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_available_current"

    @property
    def native_value(self) -> float | None:
        """Return the available charging current."""
        value: Any = self.coordinator.data.get("available_current")

        if isinstance(value, (int, float)):
            return round(float(value), 1)

        return None


class SmartChargeTargetCurrentSensor(SmartChargeBaseSensor):
    """Show the target charging current."""

    _attr_name = "Doel laadstroom"
    _attr_icon = "mdi:ev-plug-type2"
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the target-current sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_target_current"

    @property
    def native_value(self) -> int | None:
        """Return the target charging current."""
        value: Any = self.coordinator.data.get("target_current")

        if isinstance(value, (int, float)):
            return int(value)

        return None
class SmartChargeEaseeCurrentSensor(SmartChargeBaseSensor):
    """Show the current Easee charging current."""

    _attr_name = "Easee laadstroom"
    _attr_icon = "mdi:ev-plug-type2"
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Easee-current sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_easee_current"

    @property
    def native_value(self) -> float | None:
        """Return the current Easee charging current."""
        value: Any = self.coordinator.data.get("easee_current")

        if isinstance(value, (int, float)):
            return round(float(value), 1)
class SmartChargePhaseCountSensor(SmartChargeBaseSensor):
    """Show the number of charging phases."""

    _attr_name = "Aantal laadfasen"
    _attr_icon = "mdi:sine-wave"

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the phase-count sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_phase_count"

    @property
    def native_value(self) -> int | None:
        """Return the number of charging phases."""
        value: Any = self.coordinator.data.get("number_of_phases")

        if isinstance(value, int):
            return value

        return None
class SmartChargeHousePowerSensor(SmartChargeBaseSensor):
    """Show house power without the EV charger."""

    _attr_name = "Huisvermogen zonder laadpaal"
    _attr_icon = "mdi:home-lightning-bolt"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SmartChargeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the house-power sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_house_power_without_charger"

    @property
    def native_value(self) -> float | None:
        """Return house power excluding the charger."""
        value: Any = self.coordinator.data.get(
            "house_power_without_charger"
        )

        if isinstance(value, (int, float)):
            return round(float(value), 0)

        return None