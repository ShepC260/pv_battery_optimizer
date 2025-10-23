
from __future__ import annotations
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import yaml

_LOGGER = logging.getLogger(__name__)

def load_yaml(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        _LOGGER.debug("Could not load YAML %s: %s", path, e); return {}

def resolve_mappings(hass, base_path: Path, mode: str) -> Tuple[Dict[str, Any], Dict[str, bool]]:
    ents: Dict[str, str] = {}
    detected: Dict[str, bool] = {}
    detection = load_yaml(base_path / "provider_detection.yaml")
    providers = detection.get("providers", {})

    if mode == "custom":
        custom = load_yaml(base_path / "custom.yaml")
        ents.update(custom.get("entities", {}))
        detected["custom"] = True
        _LOGGER.info("[pv_battery_optimizer.detect] Using CUSTOM mappings")
        return ents, detected

    loaded = set(hass.config.components)
    _LOGGER.info("[pv_battery_optimizer.detect] AUTO provider scan (%d providers)", len(providers))

    for name, meta in providers.items():
        match = str(meta.get("match"))
        mapping_file = meta.get("mapping_file")
        detected[name] = any(match in c for c in loaded)
        if not detected[name]: continue
        data = load_yaml(base_path / mapping_file)
        ents.update(data.get("entities", {}))
        _LOGGER.debug("[pv_battery_optimizer.detect] Loaded mapping: %s", mapping_file)

    custom = load_yaml(base_path / "custom.yaml").get("entities", {})
    if custom:
        ents.update(custom); detected["custom_overrides"] = True
        _LOGGER.info("[pv_battery_optimizer.detect] Applied custom overrides")

    if "battery_soc" not in ents:
        ents.update(load_yaml(base_path / "generic_battery.yaml").get("entities", {}))
        _LOGGER.warning("[pv_battery_optimizer.detect] Missing battery_soc → applied generic_battery fallback")
    if "inverter_dc_power" not in ents:
        ents.update(load_yaml(base_path / "generic_solar.yaml").get("entities", {}))
        _LOGGER.warning("[pv_battery_optimizer.detect] Missing inverter_dc_power → applied generic_solar fallback")

    return ents, detected
