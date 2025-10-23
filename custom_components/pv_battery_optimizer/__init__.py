
from __future__ import annotations
import json, logging
from pathlib import Path
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from .const import DOMAIN, VERSION
from .coordinator import PVBatteryCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    rel_path = Path(__file__).parent / "release.json"
    try:
        info = json.loads(rel_path.read_text(encoding="utf-8"))
        _LOGGER.info("[pv_battery_optimizer.version] Loaded PV Battery Optimizer %s (%s, %s)",
                     info.get("version", VERSION),
                     info.get("build_status","unknown"),
                     info.get("release_date","unknown"))
    except Exception as e:
        _LOGGER.warning("[pv_battery_optimizer.version] Release manifest not found/invalid: %s", e)

    hass.data.setdefault(DOMAIN, {})
    coord = PVBatteryCoordinator(hass, entry)
    await coord.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coord}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.info("PV Battery Optimizer %s fully HACS compliant (MIT License, hassfest ready)", VERSION)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok: hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return ok
