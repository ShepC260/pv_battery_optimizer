
from __future__ import annotations
import json
from pathlib import Path
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, VERSION

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([ProviderSummary(entry, coord), Schedule(entry, coord), Integrations(entry, coord), VersionInfo(entry, coord)], True)

class _Base(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    def __init__(self, entry, coord):
        super().__init__(coord)
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="PV Battery Optimizer")

class ProviderSummary(_Base):
    _attr_name = "Provider Summary"; _attr_unique_id = "pv_battery_optimizer_provider_summary"; _attr_icon = "mdi:account-network"
    @property
    def native_value(self): return "Degraded" if self.coordinator.data.get("fault_latched") else "Active"
    @property
    def extra_state_attributes(self): return {"providers": self.coordinator.data.get("providers"), "fault_details": self.coordinator.data.get("fault_details")}

class Schedule(_Base):
    _attr_name = "Schedule"; _attr_unique_id = "pv_battery_optimizer_schedule"; _attr_icon = "mdi:calendar-clock"
    @property
    def native_value(self): return self.coordinator.data.get("schedule", {}).get("inverter_mode","Self-Use")
    @property
    def extra_state_attributes(self): return self.coordinator.data.get("schedule", {})

class Integrations(_Base):
    _attr_name = "Integrations"; _attr_unique_id = "pv_battery_optimizer_integrations"; _attr_icon = "mdi:puzzle-outline"
    @property
    def native_value(self): return "active"
    @property
    def extra_state_attributes(self): return self.coordinator.data.get("integrations", {})

class VersionInfo(_Base):
    _attr_name = "Version Info"; _attr_unique_id = "pv_battery_optimizer_version_info"; _attr_icon = "mdi:information-outline"
    @property
    def native_value(self): return VERSION
    @property
    def extra_state_attributes(self):
        path = Path(__file__).parent / "release.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {"version": VERSION, "channel": "unknown", "build_status": "unknown"}
        return data
