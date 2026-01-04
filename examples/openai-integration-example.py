"""
Esempio di integrazione OpenAI nel coordinator.
Copia questo codice in coordinator.py per usare ChatGPT.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from openai import OpenAI

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class AIAssistantCoordinator(DataUpdateCoordinator):
    """Class to manage fetching AI Assistant data with OpenAI."""

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
        
        # Inizializza OpenAI client
        api_key = entry.data.get("api_key")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.model = entry.data.get("model", "gpt-3.5-turbo")
            self.system_prompt = entry.data.get(
                "system_prompt",
                "You are a helpful assistant integrated with Home Assistant. "
                "Provide concise and useful responses about home automation."
            )
        else:
            self.client = None
            _LOGGER.warning("OpenAI API key not configured")

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from AI Assistant."""
        try:
            data = {
                "status": self.status,
                "last_response": self.last_response,
                "conversation_count": self.conversation_count,
                "available": self.available and self.client is not None,
                "last_update": datetime.now().isoformat(),
            }
            
            return data
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with AI Assistant: {err}")

    async def ask_question(self, question: str) -> str:
        """Ask a question to the AI assistant using OpenAI."""
        if not self.client:
            return "⚠️ API key non configurata. Configura l'API key nelle impostazioni."
        
        try:
            self.status = "thinking"
            self.async_update_listeners()
            
            # Chiama OpenAI in un executor per non bloccare
            response = await self.hass.async_add_executor_job(
                self._call_openai, question
            )
            
            self.conversation_count += 1
            self.last_response = response
            self.status = "online"
            self.async_update_listeners()
            
            _LOGGER.info(f"AI Response: {response[:100]}...")
            return response
            
        except Exception as err:
            error_msg = f"Errore: {str(err)}"
            _LOGGER.error(f"Error calling OpenAI: {err}", exc_info=True)
            self.status = "error"
            self.last_response = error_msg
            self.async_update_listeners()
            return error_msg
    
    def _call_openai(self, question: str) -> str:
        """Call OpenAI API (runs in executor to avoid blocking)."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as err:
            _LOGGER.error(f"OpenAI API error: {err}")
            raise

