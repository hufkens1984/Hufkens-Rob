"""SmartCharge BE integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import SmartChargeCoordinator


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up SmartCharge BE via YAML."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up SmartCharge BE from a config entry."""

    coordinator = SmartChargeCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload SmartCharge BE."""

    hass.data[DOMAIN].pop(entry.entry_id)

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )