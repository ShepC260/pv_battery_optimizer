
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import (
    DOMAIN, CONF_ENABLE_LOGGING, CONF_LOG_RETENTION_DAYS, CONF_MAPPING_MODE,
    DEFAULT_ENABLE_LOGGING, DEFAULT_LOG_RETENTION_DAYS, DEFAULT_MAPPING_MODE,
    MAPPING_MODE_AUTO, MAPPING_MODE_CUSTOM
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="PV Battery Optimizer",
                data={ CONF_MAPPING_MODE: user_input[CONF_MAPPING_MODE] },
                options={
                    CONF_ENABLE_LOGGING: user_input.get(CONF_ENABLE_LOGGING, DEFAULT_ENABLE_LOGGING),
                    CONF_LOG_RETENTION_DAYS: user_input.get(CONF_LOG_RETENTION_DAYS, DEFAULT_LOG_RETENTION_DAYS),
                }
            )
        schema = vol.Schema({
            vol.Required(CONF_MAPPING_MODE, default=DEFAULT_MAPPING_MODE): vol.In([MAPPING_MODE_AUTO, MAPPING_MODE_CUSTOM]),
            vol.Optional(CONF_ENABLE_LOGGING, default=DEFAULT_ENABLE_LOGGING): bool,
            vol.Optional(CONF_LOG_RETENTION_DAYS, default=DEFAULT_LOG_RETENTION_DAYS): vol.All(int, vol.Range(min=1, max=30)),
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)

class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry): self.entry = entry
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        schema = vol.Schema({
            vol.Required(CONF_MAPPING_MODE, default=self.entry.data.get(CONF_MAPPING_MODE, DEFAULT_MAPPING_MODE)): vol.In([MAPPING_MODE_AUTO, MAPPING_MODE_CUSTOM]),
            vol.Optional(CONF_ENABLE_LOGGING, default=self.entry.options.get(CONF_ENABLE_LOGGING, DEFAULT_ENABLE_LOGGING)): bool,
            vol.Optional(CONF_LOG_RETENTION_DAYS, default=self.entry.options.get(CONF_LOG_RETENTION_DAYS, DEFAULT_LOG_RETENTION_DAYS)): vol.All(int, vol.Range(min=1, max=30)),
        })
        return self.async_show_form(step_id="init", data_schema=schema)
