"""
Esempio di config_flow.py aggiornato per richiedere API key.
Copia questo codice in config_flow.py per supportare API key.
"""

"""Config flow for AI Assistant integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Schema per il primo step (base)
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="AI Assistant"): str,
        vol.Optional("update_interval", default=30): int,
    }
)

# Schema per configurazione API (secondo step)
STEP_API_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("api_key"): str,
        vol.Optional("api_provider", default="openai"): vol.In(["openai", "custom"]),
        vol.Optional("model", default="gpt-3.5-turbo"): str,
        vol.Optional("api_url"): str,  # Solo per custom
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    # Valida che l'API key sia presente se richiesta
    if data.get("api_provider") == "openai" and not data.get("api_key"):
        raise InvalidApiKey
    
    # In una implementazione reale, potresti testare la connessione qui
    # await test_api_connection(data["api_key"])
    
    return {"title": data["name"]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AI Assistant."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.user_data = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
            self.user_data = user_input
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidApiKey:
            errors["base"] = "invalid_api_key"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        if not errors:
            # Passa al secondo step per configurare l'API
            return await self.async_step_api()

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_api(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the API configuration step."""
        if user_input is None:
            return self.async_show_form(
                step_id="api", data_schema=STEP_API_DATA_SCHEMA
            )

        errors = {}

        try:
            # Valida l'API key
            if user_input.get("api_provider") == "openai":
                if not user_input.get("api_key") or len(user_input["api_key"]) < 10:
                    errors["api_key"] = "invalid_api_key"
            
            # Se custom, richiedi URL
            if user_input.get("api_provider") == "custom" and not user_input.get("api_url"):
                errors["api_url"] = "required"
                
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        if not errors:
            # Combina i dati
            combined_data = {**self.user_data, **user_input}
            
            await self.async_set_unique_id("ai_assistant")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=combined_data["name"],
                data=combined_data
            )

        return self.async_show_form(
            step_id="api", data_schema=STEP_API_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidApiKey(HomeAssistantError):
    """Error to indicate invalid API key."""

