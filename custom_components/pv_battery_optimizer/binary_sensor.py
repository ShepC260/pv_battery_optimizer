
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([Fault(entry, coord)], True)

class Fault(CoordinatorEntity, BinarySensorEntity):
    _attr_has_entity_name = True; _attr_name = "Fault"; _attr_unique_id = "pv_battery_optimizer_fault"; _attr_icon = "mdi:alert-octagon-outline"
    def __init__(self, entry, coord): super().__init__(coord); self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="PV Battery Optimizer")
    @property
    def is_on(self): return bool(self.coordinator.data.get("fault_latched"))
    @property
    def extra_state_attributes(self): return {"fault_details": self.coordinator.data.get("fault_details"), "providers": self.coordinator.data.get("providers")}
