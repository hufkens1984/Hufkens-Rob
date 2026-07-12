"""SmartCharge BE integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up via YAML."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up SmartCharge BE from a config entry."""

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

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )