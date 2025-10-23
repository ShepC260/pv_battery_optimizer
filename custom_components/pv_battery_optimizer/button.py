
from __future__ import annotations
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([Rescan(entry, coord)], True)

class Rescan(ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "Rescan Integrations & Update DCO"
    _attr_unique_id = "pv_battery_optimizer_rescan_integrations"
    _attr_icon = "mdi:refresh"

    def __init__(self, entry, coord):
        self.coordinator = coord
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="PV Battery Optimizer")

    async def async_press(self) -> None:
        _LOGGER.info("[pv_battery_optimizer.detect] Manual rescan triggered by user")
        await self.coordinator.async_rescan_integrations()
        await self.coordinator.async_run_dynamic_optimization(triggered_by="manual_rescan")
        await self.coordinator.async_request_refresh()
        detected = len(self.coordinator.detected_integrations or {})
        msg = (f"✅ PV Battery Optimizer {VERSION}\n"
               f"Rescan complete — {detected} integrations detected.\n"
               f"Dynamic Current Optimization updated successfully.")
        await self.hass.services.async_call(
            "persistent_notification", "create",
            {"title": "PV Battery Optimizer Rescan Complete", "message": msg}
        )
        _LOGGER.info("[pv_battery_optimizer.detect] Manual rescan complete (v%s, %s integrations)", VERSION, detected)
