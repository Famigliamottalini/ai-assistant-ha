"""AI Assistant Integration for Home Assistant."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS, SERVICE_ASK_QUESTION, SERVICE_RESET
from .coordinator import AIAssistantCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AI Assistant from a config entry."""
    coordinator = AIAssistantCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Register services
    async def handle_ask_question(call: ServiceCall) -> None:
        """Handle the ask question service."""
        question = call.data.get("question", "")
        _LOGGER.info(f"Question received: {question}")
        
        # Simula una risposta (in una implementazione reale, chiameresti l'API AI)
        response = f"Risposta alla domanda: {question}"
        coordinator.update_conversation(response)
        
        hass.bus.async_fire(
            "ai_assistant_response",
            {"question": question, "response": response}
        )
    
    async def handle_reset(call: ServiceCall) -> None:
        """Handle the reset service."""
        coordinator.conversation_count = 0
        coordinator.last_response = "Reset"
        await coordinator.async_request_refresh()
    
    hass.services.async_register(DOMAIN, SERVICE_ASK_QUESTION, handle_ask_question)
    hass.services.async_register(DOMAIN, SERVICE_RESET, handle_reset)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
