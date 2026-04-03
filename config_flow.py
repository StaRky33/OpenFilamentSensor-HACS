"""Config flow for Open Filament Sensor."""
from __future__ import annotations

import logging
import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, API_ENDPOINT, CONF_DEVICE_NAME, CONF_CAMERA_ENTITY

_LOGGER = logging.getLogger(__name__)


async def _validate_host(host: str) -> bool:
    """Try to reach the OFS device."""
    url = f"http://{host}{API_ENDPOINT}"
    try:
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
    except Exception:
        return False


class OFSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Open Filament Sensor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Step 1: Enter device IP and custom name."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            device_name = user_input[CONF_DEVICE_NAME].strip()

            # Prevent duplicate entries for the same host
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            if not await _validate_host(host):
                errors["base"] = "cannot_connect"
            else:
                # Store and move to camera step
                self._host = host
                self._device_name = device_name
                return await self.async_step_camera()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_DEVICE_NAME, default="Open Filament Sensor"): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "host_example": "192.168.1.25",
            },
        )

    async def async_step_camera(self, user_input=None):
        """Step 2: Optionally link an Elegoo camera entity."""
        if user_input is not None:
            return self.async_create_entry(
                title=self._device_name,
                data={
                    CONF_HOST: self._host,
                    CONF_DEVICE_NAME: self._device_name,
                    CONF_CAMERA_ENTITY: user_input.get(CONF_CAMERA_ENTITY, ""),
                },
            )

        # Build list of available camera entities
        camera_entities = [
            selector.SelectOptionDict(value="", label="— None —")
        ] + [
            selector.SelectOptionDict(value=state.entity_id, label=state.name or state.entity_id)
            for state in self.hass.states.async_all("camera")
        ]

        return self.async_show_form(
            step_id="camera",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_CAMERA_ENTITY): selector.SelectSelector(
                        selector.SelectSelectorConfig(options=camera_entities)
                    ),
                }
            ),
        )
