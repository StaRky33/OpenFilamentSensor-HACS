"""DataUpdateCoordinator for Open Filament Sensor."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_ENDPOINT, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class OFSDataCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from the OFS device."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.host = host
        self.url = f"http://{host}{API_ENDPOINT}"

    async def _async_update_data(self) -> dict:
        """Fetch data from the OFS device."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as response:
                        if response.status != 200:
                            raise UpdateFailed(
                                f"OFS device returned status {response.status}"
                            )
                        return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with OFS device: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error fetching OFS data: {err}") from err
