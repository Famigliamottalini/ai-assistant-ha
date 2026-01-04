"""Data update coordinator for AI Assistant."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class AIAssistantCoordinator(DataUpdateCoordinator):
    """Class to manage fetching AI Assistant data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_UPDATE_INTERVAL,
        )
        self.entry = entry
        self.conversation_count = 0
        self.last_response = "Ready"
        self.status = "online"
        self.available = True

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from AI Assistant."""
        try:
            # Simula il recupero dei dati dell'AI
            # In una implementazione reale, qui faresti una chiamata API
            data = {
                "status": self.status,
                "last_response": self.last_response,
                "conversation_count": self.conversation_count,
                "available": self.available,
                "last_update": datetime.now().isoformat(),
            }
            
            return data
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with AI Assistant: {err}")

    def update_conversation(self, response: str) -> None:
        """Update conversation data."""
        self.conversation_count += 1
        self.last_response = response
        self.async_update_listeners()

